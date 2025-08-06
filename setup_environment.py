#!/usr/bin/env python3
"""
Script de configuration de l'environnement pour OpenFoodFacts Pipeline
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Cree le fichier .env a partir de l'exemple"""
    config_dir = Path("config")
    env_example = config_dir / "env_example.txt"
    env_file = config_dir / ".env"
    
    if not config_dir.exists():
        print("Dossier config non trouve. Creation...")
        config_dir.mkdir()
    
    if env_file.exists():
        print("Fichier .env existe deja.")
        response = input("Voulez-vous le remplacer ? (o/n) : ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("Configuration annulee.")
            return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"Fichier .env cree : {env_file}")
        print("Modifiez le fichier .env avec vos vraies valeurs.")
    else:
        print("Fichier env_example.txt non trouve.")
        create_env_file_manual(env_file)

def create_env_file_manual(env_file):
    """Cree le fichier .env manuellement"""
    content = """# Configuration OpenFoodFacts Pipeline
# Modifiez ces valeurs avec vos vraies credentials

# Google Cloud Platform
GOOGLE_APPLICATION_CREDENTIALS_PATH=path/to/your/credentials.json
GOOGLE_CLOUD_PROJECT_ID=project-final-laka-93110
GOOGLE_CLOUD_DATASET_ID=Laka10
GOOGLE_CLOUD_TABLE_ID=openfoodfacts

# API Configuration
OPENFOODFACTS_API_URL=https://world.openfoodfacts.org
OPENFOODFACTS_PAGE_SIZE=1000
OPENFOODFACTS_NUM_PAGES=20

# File Paths
DATA_DIRECTORY=data
CSV_ORIGINAL_FILENAME=openfood_referentiel.csv
CSV_CLEANED_FILENAME=openfood_referentiel_cleaned.csv
CSV_TRANSFORMED_FILENAME=openfood_transformed.csv
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fichier .env cree manuellement : {env_file}")

def check_credentials():
    """Verifie si les credentials existent"""
    possible_paths = [
        "project-final-laka-93110-e98c1369c8cc.json",
        "config/project-final-laka-93110-e98c1369c8cc.json",
        r"C:\Users\dthia\Desktop\Project_openfoodfacts\Project_openfoodfacts\project-final-laka-93110-e98c1369c8cc.json",
        "/mnt/c/Users/dthia/Desktop/Project_openfoodfacts/Project_openfoodfacts/project-final-laka-93110-e98c1369c8cc.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Credentials trouves : {path}")
            return path
    
    print("Aucun fichier de credentials trouve.")
    return None

def setup_directories():
    """Cree les dossiers necessaires"""
    directories = ["data", "config"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Dossier cree : {directory}")
        else:
            print(f"Dossier existe deja : {directory}")

def main():
    """Fonction principale"""
    print("Configuration de l'environnement OpenFoodFacts Pipeline")
    print("=" * 50)
    
    # Creer les dossiers
    print("\n1. Creation des dossiers...")
    setup_directories()
    
    # Verifier les credentials
    print("\n2. Verification des credentials...")
    credentials_path = check_credentials()
    
    # Creer le fichier .env
    print("\n3. Configuration du fichier .env...")
    create_env_file()
    
    # Instructions finales
    print("\n" + "=" * 50)
    print("Configuration terminee !")
    print("\nProchaines etapes :")
    print("1. Modifiez le fichier config/.env avec vos vraies valeurs")
    print("2. Assurez-vous que vos credentials Google Cloud sont en place")
    print("3. Installez les dependances : pip install -r requirements.txt")
    print("4. Testez la configuration : python test_pipeline.py")
    print("5. Lancez le pipeline : python openfoodfacts_pipeline.py")

if __name__ == "__main__":
    main() 