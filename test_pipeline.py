import pandas as pd
import os
from google.cloud import bigquery

# Import de la configuration
try:
    from config.config import get_config, get_google_credentials_path
    config = get_config()
    print("Configuration chargee depuis config/config.py")
except ImportError:
    print("Module config non trouve. Utilisation de la configuration par defaut.")
    config = {
        'google_cloud': {
            'project_id': 'project-final-laka-93110',
            'dataset_id': 'Laka10',
            'table_id': 'openfoodfacts'
        },
        'api': {
            'url': 'https://world.openfoodfacts.org',
            'page_size': 1000,
            'num_pages': 20
        },
        'files': {
            'data_directory': 'data',
            'csv_original_filename': 'openfood_referentiel.csv',
            'csv_cleaned_filename': 'openfood_referentiel_cleaned.csv',
            'csv_transformed_filename': 'openfood_transformed.csv'
        },
        'credentials_path': None
    }

# Configuration depuis les variables d'environnement ou valeurs par defaut
DATA_DIR = config['files']['data_directory']

def get_credentials_path():
    """Retourne le chemin vers le fichier de credentials"""
    if config.get('credentials_path'):
        return config['credentials_path']
    
    # Utiliser la fonction du module config si disponible
    try:
        from config.config import get_google_credentials_path
        return get_google_credentials_path()
    except ImportError:
        pass
    
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

def get_csv_path(filename):
    """Retourne le chemin complet pour un fichier CSV dans le dossier data"""
    return os.path.join(DATA_DIR, filename)

def test_csv_loading(csv_path):
    """Teste le chargement du fichier CSV"""
    print(f"Test de chargement du fichier CSV : {csv_path}")
    
    if not csv_path or not os.path.exists(csv_path):
        print(f"Fichier introuvable : {csv_path}")
        return False
    
    try:
        # Charger le fichier CSV
        df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
        print(f"Fichier CSV charge avec succes : {len(df)} lignes")
        
        # Verifier les colonnes
        print(f"Colonnes trouvees : {list(df.columns)}")
        
        # Verifier les types de donnees
        print("Types de donnees :")
        for col, dtype in df.dtypes.items():
            print(f"  - {col}: {dtype}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return False

def test_bigquery_connection():
    """Teste la connexion a BigQuery"""
    print("Test de connexion a BigQuery")
    
    # Verifier si le fichier de credentials existe
    credentials_path = get_credentials_path()
    if not credentials_path:
        print("Fichier de credentials GCP non trouve")
        return False
    
    try:
        # Configurer les credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        client = bigquery.Client()
        print("Connexion a BigQuery etablie")
        
        # Tester une requete simple
        query = "SELECT 1 as test"
        result = client.query(query).result()
        print("Requete de test reussie")
        
        return True
        
    except Exception as e:
        print(f"Erreur de connexion a BigQuery : {e}")
        return False

def test_data_quality(csv_path):
    """Teste la qualite des donnees"""
    print("Test de qualite des donnees")
    
    if not csv_path or not os.path.exists(csv_path):
        print(f"Fichier CSV introuvable : {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
        
        # Verifier les valeurs manquantes
        missing_data = df.isnull().sum()
        print("Valeurs manquantes par colonne :")
        for col, missing in missing_data.items():
            if missing > 0:
                print(f"  - {col}: {missing} ({missing/len(df)*100:.1f}%)")
        
        # Verifier les doublons
        duplicates = df.duplicated().sum()
        print(f"Doublons trouves : {duplicates}")
        
        # Verifier les colonnes numeriques
        numeric_cols = ['energy_kcal', 'fat_100g', 'sugars_100g', 'proteins_100g']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                valid_values = df[col].notna().sum()
                print(f"  - {col}: {valid_values} valeurs valides sur {len(df)}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test de qualite : {e}")
        return False

def test_data_directory():
    """Teste la structure du dossier data"""
    print("Test de la structure du dossier data")
    
    if not os.path.exists(DATA_DIR):
        print(f"Dossier {DATA_DIR} non trouve")
        return False
    
    print(f"Dossier {DATA_DIR} trouve")
    
    # Lister les fichiers dans le dossier data
    files = os.listdir(DATA_DIR)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    print(f"Fichiers CSV trouves dans {DATA_DIR} :")
    for file in csv_files:
        file_path = os.path.join(DATA_DIR, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
    
    return len(csv_files) > 0

def test_configuration():
    """Teste la configuration"""
    print("Test de la configuration")
    
    try:
        # Verifier que la configuration est chargee
        if config:
            print("Configuration chargee avec succes")
            
            # Afficher les parametres principaux
            print(f"  - Dossier data : {config['files']['data_directory']}")
            print(f"  - Projet Google Cloud : {config['google_cloud']['project_id']}")
            print(f"  - Dataset : {config['google_cloud']['dataset_id']}")
            print(f"  - Table : {config['google_cloud']['table_id']}")
            print(f"  - URL API : {config['api']['url']}")
            print(f"  - Taille page : {config['api']['page_size']}")
            print(f"  - Nombre pages : {config['api']['num_pages']}")
            
            return True
        else:
            print("Configuration non chargee")
            return False
            
    except Exception as e:
        print(f"Erreur lors du test de configuration : {e}")
        return False

def main():
    """Fonction principale de test"""
    print("Debut des tests du pipeline OpenFoodFacts")
    print("=" * 50)
    
    # Test 0: Configuration
    print("\n0. Test de la configuration")
    test0 = test_configuration()
    
    # Test 1: Structure du dossier data
    print("\n1. Test de la structure du dossier data")
    test1 = test_data_directory()
    
    # Chemins des fichiers
    csv_path = get_csv_path(config['files']['csv_original_filename'])
    cleaned_csv_path = get_csv_path(config['files']['csv_cleaned_filename'])
    transformed_csv_path = get_csv_path(config['files']['csv_transformed_filename'])
    
    # Test 2: Chargement du fichier CSV original
    print("\n2. Test du fichier CSV original")
    test2 = test_csv_loading(csv_path)
    
    # Test 3: Chargement du fichier CSV nettoye (s'il existe)
    print("\n3. Test du fichier CSV nettoye")
    test3 = test_csv_loading(cleaned_csv_path) if cleaned_csv_path else False
    
    # Test 4: Chargement du fichier CSV transforme (s'il existe)
    print("\n4. Test du fichier CSV transforme")
    test4 = test_csv_loading(transformed_csv_path) if transformed_csv_path else False
    
    # Test 5: Connexion a BigQuery
    print("\n5. Test de la connexion BigQuery")
    test5 = test_bigquery_connection()
    
    # Test 6: Qualite des donnees
    print("\n6. Test de la qualite des donnees")
    test6 = test_data_quality(csv_path if test2 else cleaned_csv_path)
    
    # Resume des tests
    print("\n" + "=" * 50)
    print("Resume des tests :")
    print(f"  Configuration : {'OK' if test0 else 'ECHEC'}")
    print(f"  Structure dossier data : {'OK' if test1 else 'ECHEC'}")
    print(f"  CSV original : {'OK' if test2 else 'ECHEC'}")
    print(f"  CSV nettoye : {'OK' if test3 else 'N/A'}")
    print(f"  CSV transforme : {'OK' if test4 else 'N/A'}")
    print(f"  BigQuery : {'OK' if test5 else 'ECHEC'}")
    print(f"  Qualite donnees : {'OK' if test6 else 'ECHEC'}")
    
    if all([test0, test1, test2, test5, test6]):
        print("\nTous les tests sont passes avec succes !")
    else:
        print("\nCertains tests ont echoue. Verifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main() 