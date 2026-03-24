📑 LayoutLM Document Classifier
Ce projet est une solution complète de classification intelligente de documents (Factures vs Autres) basée sur l'architecture multimodale LayoutLM. Contrairement au NLP classique, ce modèle analyse à la fois le texte (OCR) et la structure spatiale (coordonnées 2D) des documents.

🚀 Fonctionnalités
Pipeline End-to-End : Du téléchargement des données à l'API de production.

OCR Intégré : Utilisation de Tesseract pour l'extraction de texte et des positions.

Tri Automatique : Classement des documents dans des dossiers avec un seuil de confiance.

Analyse Statistique : Génération de rapports CSV et graphiques de distribution de confiance.

Déploiement Docker : API FastAPI prête pour le Cloud.

🛠️ Installation
1. Prérequis système
Vous devez avoir Tesseract OCR et Poppler installés sur votre machine :

Bash
# Ubuntu / Debian
sudo apt-get install tesseract-ocr poppler-utils
2. Installation Python
Bash
pip install -r requirements.txt
📂 Structure du Projet
data/layouts/ : Dossier contenant les documents d'entraînement (PDF).

layoutlm_manual_final/ : Modèle entraîné et mapping des labels.

api_script.py : Serveur FastAPI pour l'inférence en temps réel.

Dockerfile : Configuration pour la conteneurisation.

🧠 Entraînement et Tri
Pour entraîner le modèle sur 100% de votre dataset et organiser vos fichiers :

Placez vos PDFs dans data/layouts/.

Lancez le script d'entraînement global.

Le script générera un dossier documents_tries/ avec une section A_VERIFIER pour les documents dont la confiance est inférieure à 85%.

🐳 Déploiement (Docker)
Pour lancer l'API de classification dans un conteneur isolé :

Bash
# Construire l'image
docker build -t layoutlm-api .

# Lancer le conteneur
docker run -p 8000:8000 layoutlm-api
L'API sera disponible sur http://localhost:8000/docs.

📊 Performance
Le modèle utilise l'optimiseur AdamW pour une meilleure généralisation. Vous pouvez visualiser la fiabilité du tri via l'histogramme de distribution généré automatiquement