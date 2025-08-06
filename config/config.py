import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
def load_environment():
    """Charge les variables d'environnement depuis le fichier .env"""
    # Chercher le fichier .env dans le dossier config
    config_dir = Path(__file__).parent
    env_file = config_dir / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Variables d'environnement chargees depuis : {env_file}")
    else:
        print("Fichier .env non trouve. Utilisation des variables d'environnement systeme.")

# Configuration Google Cloud Platform
def get_google_credentials_path():
    """Retourne le chemin vers le fichier de credentials Google Cloud"""
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_PATH')
    
    if credentials_path:
        # Si le chemin est relatif, le rendre absolu
        if not os.path.isabs(credentials_path):
            config_dir = Path(__file__).parent
            credentials_path = config_dir / credentials_path
            
        if os.path.exists(credentials_path):
            return str(credentials_path)
    
    # Fallback : chercher le fichier dans les emplacements habituels
    possible_paths = [
        "/mnt/c/Users/dthia/Desktop/Project_openfoodfacts/Project_openfoodfacts/project-final-laka-93110-e98c1369c8cc.json",
        r"C:\Users\dthia\Desktop\Project_openfoodfacts\Project_openfoodfacts\project-final-laka-93110-e98c1369c8cc.json",
        "project-final-laka-93110-e98c1369c8cc.json",
        os.path.join(os.getcwd(), "project-final-laka-93110-e98c1369c8cc.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_google_cloud_config():
    """Retourne la configuration Google Cloud"""
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'project-final-laka-93110'),
        'dataset_id': os.getenv('GOOGLE_CLOUD_DATASET_ID', 'Laka10'),
        'table_id': os.getenv('GOOGLE_CLOUD_TABLE_ID', 'openfoodfacts')
    }

# Configuration API
def get_api_config():
    """Retourne la configuration de l'API"""
    return {
        'url': os.getenv('OPENFOODFACTS_API_URL', 'https://world.openfoodfacts.org'),
        'page_size': int(os.getenv('OPENFOODFACTS_PAGE_SIZE', '1000')),
        'num_pages': int(os.getenv('OPENFOODFACTS_NUM_PAGES', '20'))
    }

# Configuration des fichiers
def get_file_config():
    """Retourne la configuration des fichiers"""
    return {
        'data_directory': os.getenv('DATA_DIRECTORY', 'data'),
        'csv_original_filename': os.getenv('CSV_ORIGINAL_FILENAME', 'openfood_referentiel.csv'),
        'csv_cleaned_filename': os.getenv('CSV_CLEANED_FILENAME', 'openfood_referentiel_cleaned.csv'),
        'csv_transformed_filename': os.getenv('CSV_TRANSFORMED_FILENAME', 'openfood_transformed.csv')
    }

# Configuration complète
def get_config():
    """Retourne toute la configuration"""
    return {
        'google_cloud': get_google_cloud_config(),
        'api': get_api_config(),
        'files': get_file_config(),
        'credentials_path': get_google_credentials_path()
    }

# Initialiser la configuration au chargement du module
load_environment() 