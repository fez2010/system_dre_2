# Install Wget (the GNU version)
winget install GNU.Wget  --silent

# Install Python (if not already present)
winget install Python.Python.3.12 --silent
winget install UB-Mannheim.TesseractOCR --silent
winget install oschwartz10612.Poppler --silent

# Update Path for the current session so Tesseract is immediately available
$env:Path += ";C:\Program Files\Tesseract-OCR"