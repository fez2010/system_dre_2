import torch
import pytesseract
import json
import io
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from pdf2image import convert_from_bytes
from transformers import LayoutLMForSequenceClassification, LayoutLMTokenizer

# --- 1. CONFIGURATION & CHARGEMENT ---
app = FastAPI(title="LayoutLM Document Classifier API")
MODEL_PATH = "./layoutlm_manual_final"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Chargement du dictionnaire de labels
with open(f"{MODEL_PATH}/mapping_labels.json", "r") as f:
    id2label = {int(k): v for k, v in json.load(f).items()}

tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
model = LayoutLMForSequenceClassification.from_pretrained(MODEL_PATH).to(DEVICE)
model.eval()

# --- 2. FONCTIONS DE PRÉTRAITEMENT ---
def normalize_bbox(bbox, w, h):
    return [
        max(0, min(int(1000 * (bbox[0] / w)), 999)),
        max(0, min(int(1000 * (bbox[1] / h)), 999)),
        max(0, min(int(1000 * ((bbox[0] + bbox[2]) / w)), 999)),
        max(0, min(int(1000 * ((bbox[1] + bbox[3]) / h)), 999))
    ]

def prepare_features(words, bboxes, max_len=512):
    token_ids, token_boxes = [], []
    for word, box in zip(words, bboxes):
        word_tokens = tokenizer.encode(word, add_special_tokens=False)
        token_ids.extend(word_tokens)
        token_boxes.extend([box] * len(word_tokens))
    
    token_ids = [tokenizer.cls_token_id] + token_ids[:max_len-2] + [tokenizer.sep_token_id]
    token_boxes = [[0, 0, 0, 0]] + token_boxes[:max_len-2] + [[0, 0, 0, 0]]
    pad_len = max_len - len(token_ids)
    
    return {
        "input_ids": torch.tensor(token_ids + [tokenizer.pad_token_id] * pad_len).unsqueeze(0).to(DEVICE),
        "bbox": torch.tensor(token_boxes + [[0, 0, 0, 0]] * pad_len).unsqueeze(0).to(DEVICE),
        "attention_mask": torch.tensor([1] * (max_len - pad_len) + [0] * pad_len).unsqueeze(0).to(DEVICE)
    }

# --- 3. POINT D'ENTRÉE (ENDPOINT) ---
@app.post("/predict")
async def predict_document(file: UploadFile = File(...)):
    # Lecture du fichier (PDF ou Image)
    content = await file.read()
    
    if file.content_type == "application/pdf":
        pages = convert_from_bytes(content, dpi=200, first_page=1, last_page=1)
        image = pages[0]
    else:
        image = Image.open(io.BytesIO(content)).convert("RGB")
    
    # OCR & Layout Analysis
    w, h = image.size
    ocr = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    words, bboxes = [], []
    for j, text in enumerate(ocr['text']):
        if text.strip() and int(ocr['conf'][j]) > 15:
            words.append(text)
            bboxes.append(normalize_bbox([ocr['left'][j], ocr['top'][j], ocr['width'][j], ocr['height'][j]], w, h))
    
    if not words:
        return {"error": "Aucun texte détecté"}

    # Inférence
    inputs = prepare_features(words, bboxes)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        conf, idx = torch.max(probs, dim=-1)
    
    return {
        "filename": file.filename,
        "prediction": id2label.get(idx.item()),
        "confidence": float(conf.item()),
        "status": "VALID" if conf.item() > 0.85 else "UNCERTAIN"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)