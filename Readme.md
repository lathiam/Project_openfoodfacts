# OpenFoodFacts Pipeline

Pipeline ETL pour collecter, transformer et analyser les données de l'API OpenFoodFacts avec intégration BigQuery.

## 🚀 Installation rapide

```bash
# 1. Cloner le projet
git clone <repository-url>
cd Project_openfoodfacts

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'environnement
python setup_environment.py

# 4. Lancer le pipeline
python openfoodfacts_pipeline.py
```

## 📁 Structure

```
Project_openfoodfacts/
├── config/                    # Configuration et variables d'environnement
├── data/                      # Fichiers CSV générés
├── openfoodfacts_pipeline.py  # Pipeline principal
├── test_pipeline.py          # Tests
└── setup_environment.py      # Configuration automatique
```

## ⚙️ Configuration

1. **Créer le fichier de configuration** :
```bash
cp config/env_example.txt config/.env
```

2. **Modifier `config/.env`** avec vos credentials :
```env
GOOGLE_APPLICATION_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_DATASET_ID=your-dataset
GOOGLE_CLOUD_TABLE_ID=your-table
```

## 🎯 Utilisation

### Pipeline complet
```bash
python openfoodfacts_pipeline.py
```

### Tests
```bash
python test_pipeline.py
```

### Vérification des imports
```bash
python check_imports.py
```

## 🔧 Fonctionnalités

- **Extraction** : Récupération des données depuis l'API OpenFoodFacts
- **Transformation** : Nettoyage, traductions, scores nutritionnels
- **Chargement** : Intégration dans Google BigQuery
- **Sauvegarde** : Fichiers CSV organisés dans `data/`

## 🔒 Sécurité

- Variables d'environnement dans `config/.env` (protégé par .gitignore)
- Credentials Google Cloud sécurisés
- Fichiers sensibles exclus du versioning

## 📊 Données générées

- `data/openfood_referentiel.csv` : Données brutes
- `data/openfood_referentiel_cleaned.csv` : Données nettoyées
- `data/openfood_transformed.csv` : Données transformées

## 🐛 Troubleshooting

### Problème de configuration
```bash
python setup_environment.py
```

### Problème de credentials
1. Vérifiez que le fichier de credentials existe
2. Vérifiez le chemin dans `config/.env`
3. Vérifiez les permissions du fichier

### Problème de dépendances
```bash
pip install -r requirements.txt
```
