import requests
import pandas as pd
import time
import os
import re
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
PAGE_SIZE = config['api']['page_size']
NUM_PAGES = config['api']['num_pages']

# Configuration BigQuery
PROJECT_ID = config['google_cloud']['project_id']
DATASET_ID = config['google_cloud']['dataset_id']
TABLE_ID = config['google_cloud']['table_id']
BQ_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Création du dossier data s'il n'existe pas
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Dossier {DATA_DIR} cree")

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
            print(f"Fichier de credentials trouve : {path}")
            return path
    
    print("Fichier de credentials non trouve")
    return None

def get_csv_path(filename):
    """Retourne le chemin complet pour un fichier CSV dans le dossier data"""
    return os.path.join(DATA_DIR, filename)

def check_api_connection():
    """Verifie la connexion a l'API OpenFoodFacts"""
    try:
        response = requests.get(config['api']['url'], timeout=5)
        if response.status_code == 200:
            print("Connexion a l'API OpenFoodFacts etablie")
            return True
    except Exception as e:
        print(f"Echec de connexion a l'API : {e}")
    return False

def fetch_products(page, page_size=None):
    """Recupere les produits d'une page donnee"""
    if page_size is None:
        page_size = PAGE_SIZE
    
    url = f"{config['api']['url']}/cgi/search.pl"
    params = {
        "action": "process",
        "page_size": page_size,
        "page": page,
        "json": True,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur HTTP page {page} : {e}")
    except ValueError as e:
        print(f"Erreur JSON page {page} : {e}")
    return []

def extract_product_info(product):
    """Extrait les informations d'un produit"""
    return {
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "stores": product.get("stores", ""),
        "nutriscore_grade": product.get("nutriscore_grade", ""),
        "nutrition_score_fr": product.get("nutrition_score_fr", ""),
        "energy_kcal": product.get("nutriments", {}).get("energy-kcal_100g"),
        "fat_100g": product.get("nutriments", {}).get("fat_100g"),
        "saturated_fat_100g": product.get("nutriments", {}).get("saturated-fat_100g"),
        "sugars_100g": product.get("nutriments", {}).get("sugars_100g"),
        "salt_100g": product.get("nutriments", {}).get("salt_100g"),
        "fiber_100g": product.get("nutriments", {}).get("fiber_100g"),
        "proteins_100g": product.get("nutriments", {}).get("proteins_100g"),
        "labels": product.get("labels", ""),
        "origins": product.get("origins", ""),
        "categories": product.get("categories", ""),
        "url": product.get("url", ""),
        "code": product.get("code", ""),
    }

def clean_text(text):
    """Nettoie le texte pour eviter les problemes de CSV"""
    if pd.isna(text) or text is None:
        return ""
    
    text = str(text)
    # Supprimer les caracteres de controle
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # Remplacer les guillemets doubles par des guillemets simples
    text = text.replace('"', "'")
    # Supprimer les retours a la ligne et tabulations
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    # Limiter la longueur
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    return text

def clean_column_name(col):
    """Nettoie les noms de colonnes"""
    col = col.strip()
    col = re.sub(r"[^\w]", "_", col)
    col = re.sub(r"__+", "_", col)
    return col.strip("_")

def translate_text(text):
    """Traduit le texte de l'anglais vers le francais"""
    translations = {
        "organic": "bio",
        "gluten-free": "sans gluten",
        "vegetarian": "vegetarien",
        "vegan": "vegetalien",
        "non-gmo": "sans OGM",
        "halal": "halal",
        "kosher": "kasher",
        "beverages": "boissons",
        "dairies": "produits laitiers",
        "sodas": "sodas",
        "snacks": "snacks",
        "cereals": "cereales",
        "meats": "viandes",
        "ready-meals": "plats prepares",
        "breakfasts": "petits-dejeuners",
        "cheeses": "fromages",
        "desserts": "desserts",
        "france": "France",
        "germany": "Allemagne",
        "italy": "Italie",
        "spain": "Espagne",
        "carrefour": "Carrefour",
        "leclerc": "Leclerc",
        "lidl": "Lidl",
        "auchan": "Auchan",
        "monoprix": "Monoprix"
    }
    
    for eng, fr in translations.items():
        text = re.sub(rf"\b{eng}\b", fr, text, flags=re.IGNORECASE)
    return text

def transliterate_text(text):
    """Translitere le texte arabe vers le francais"""
    arabic_to_french = {
        "سلطان": "Sultan",
        "الراية": "Al-Raya",
        "كارفور": "Carrefour",
        "أوشان": "Auchan",
        "ليدل": "Lidl"
    }
    
    for ar, fr in arabic_to_french.items():
        text = re.sub(rf"\b{ar}\b", fr, text)
    return text

def classify_nutriscore(score):
    """Classifie le nutriscore"""
    score = str(score).strip().upper()
    classifications = {
        "A": "Excellent",
        "B": "Bon",
        "C": "Moyen",
        "D": "Mediocre",
        "E": "Mauvais"
    }
    return classifications.get(score, "Inconnu")

def clean_csv_file(input_path, output_path):
    """Nettoie un fichier CSV existant"""
    print(f"Chargement du fichier : {input_path}")
    
    try:
        # Charger le fichier CSV
        df = pd.read_csv(input_path, encoding='utf-8', on_bad_lines='skip')
        print(f"{len(df)} lignes chargees")
        
        # Nettoyer toutes les colonnes textuelles
        text_columns = df.select_dtypes(include=['object']).columns
        print(f"Nettoyage de {len(text_columns)} colonnes textuelles")
        
        for col in text_columns:
            df[col] = df[col].apply(clean_text)
        
        # Nettoyer les colonnes numeriques
        numeric_columns = ['energy_kcal', 'fat_100g', 'saturated_fat_100g', 'sugars_100g', 
                          'salt_100g', 'fiber_100g', 'proteins_100g', 'nutrition_score_fr']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Supprimer les lignes avec trop de valeurs manquantes
        min_required = len(df.columns) * 0.3
        df_cleaned = df.dropna(thresh=min_required)
        print(f"{len(df_cleaned)} lignes conservees apres nettoyage")
        
        # Sauvegarder
        df_cleaned.to_csv(output_path, index=False, encoding='utf-8', quoting=1)
        print(f"Fichier nettoye sauvegarde : {output_path}")
        
        return df_cleaned
        
    except Exception as e:
        print(f"Erreur lors du nettoyage : {e}")
        return None

def save_to_csv(df, path):
    """Sauvegarde le DataFrame en CSV avec nettoyage"""
    print("Nettoyage des donnees avant sauvegarde")
    
    # Nettoyer les noms de colonnes
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Nettoyer toutes les colonnes textuelles
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].apply(clean_text)
    
    # Nettoyer les colonnes numeriques
    numeric_columns = ['energy_kcal', 'fat_100g', 'saturated_fat_100g', 'sugars_100g', 
                      'salt_100g', 'fiber_100g', 'proteins_100g', 'nutrition_score_fr']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Supprimer les lignes avec trop de valeurs manquantes
    df = df.dropna(thresh=len(df.columns) * 0.3)
    
    # Sauvegarder
    df.to_csv(path, index=False, encoding='utf-8', quoting=1)
    print(f"Fichier CSV sauvegarde : {path}")

def load_to_bigquery(csv_path, table_id):
    """Charge les donnees dans BigQuery"""
    credentials_path = get_credentials_path()
    if not credentials_path:
        print("Impossible de charger dans BigQuery : fichier de credentials non trouve")
        return
    
    try:
        client = bigquery.Client()
        print("Connexion BigQuery etablie")
        
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition="WRITE_TRUNCATE",
            max_bad_records=10,
            ignore_unknown_values=True
        )
        
        with open(csv_path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        print(f"Donnees chargees dans BigQuery : {table_id}")
    except Exception as e:
        print(f"Erreur lors du chargement dans BigQuery : {e}")

def get_data_from_bigquery(table_id):
    """Recupere les donnees depuis BigQuery"""
    credentials_path = get_credentials_path()
    if not credentials_path:
        print("Impossible de recuperer depuis BigQuery : fichier de credentials non trouve")
        return pd.DataFrame()
    
    try:
        client = bigquery.Client()
        query = f"SELECT * FROM `{table_id}`"
        df = client.query(query).to_dataframe()
        print(f"{len(df)} lignes recuperees depuis BigQuery")
        return df
    except Exception as e:
        print(f"Erreur lors de la recuperation depuis BigQuery : {e}")
        return pd.DataFrame()

def transform_data(df):
    """Transforme les donnees avec toutes les fonctionnalites"""
    if df.empty:
        print("DataFrame vide : aucune transformation possible")
        return df

    print("Transformation des donnees")

    # Conversion des colonnes numeriques
    numeric_cols = ['energy_kcal', 'fat_100g', 'sugars_100g', 'proteins_100g', 
                   'fiber_100g', 'salt_100g', 'saturated_fat_100g']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Nettoyage des donnees textuelles
    df['nutriscore_grade'] = df['nutriscore_grade'].fillna("").str.upper()
    df['product_name'] = df['product_name'].fillna("Inconnu")
    
    # Nettoyage des colonnes textuelles
    for col in ["labels", "brands", "categories", "origins", "stores"]:
        if col in df.columns:
            df[col] = df[col].fillna("").str.lower().str.strip()
    
    # Suppression des lignes inutiles
    df = df[df["product_name"].str.lower() != "inconnu"]
    min_non_null = len(df.columns) * 0.5
    df = df.dropna(thresh=min_non_null)
    
    # Suppression des lignes avec trop de valeurs manquantes
    important_cols = ["energy_kcal", "sugars_100g", "saturated_fat_100g", "proteins_100g", "fiber_100g"]
    available_cols = [col for col in important_cols if col in df.columns]
    if available_cols:
        df = df.dropna(subset=available_cols)
    
    # Traductions et translitteration
    for col in ["labels", "categories", "stores", "brands", "origins"]:
        if col in df.columns:
            df[col] = df[col].apply(translate_text)
            df[col] = df[col].apply(transliterate_text)
            df[col] = df[col].str.title().str.strip()
    
    # Ajout de colonnes derivees
    df['has_label_bio'] = df['labels'].str.contains("bio", case=False, na=False)

    # Calcul de la densite nutritionnelle
    df["nutrient_density"] = df["energy_kcal"] / (
        df["proteins_100g"].fillna(0) +
        df["fat_100g"].fillna(0) +
        df["sugars_100g"].fillna(0)
    ).replace([0, float('inf')], 1)
    
    # Scoring nutritionnel personnalise
    df["scoring_nutritionnel_personnalise"] = (
        df["energy_kcal"].fillna(0) + 
        df["sugars_100g"].fillna(0) + 
        df["saturated_fat_100g"].fillna(0) -
        (df["proteins_100g"].fillna(0) + df["fiber_100g"].fillna(0))
    )
    
    # Classification de la qualite nutritionnelle
    df["qualite_nutritionnelle"] = df["nutriscore_grade"].apply(classify_nutriscore)

    print("Donnees transformees")
    return df

def main():
    """Pipeline principal"""
    if not check_api_connection():
        print("Arret du pipeline car l'API OpenFoodFacts est injoignable")
        return

    # Chemins des fichiers
    csv_path = get_csv_path(config['files']['csv_original_filename'])
    cleaned_csv_path = get_csv_path(config['files']['csv_cleaned_filename'])
    transformed_csv_path = get_csv_path(config['files']['csv_transformed_filename'])

    # Verifier si un fichier CSV existe deja
    if os.path.exists(csv_path):
        print(f"Fichier CSV existant trouve : {csv_path}")
        print("Nettoyage du fichier CSV existant")
        cleaned_df = clean_csv_file(csv_path, cleaned_csv_path)
        if cleaned_df is not None:
            print("Fichier CSV nettoye avec succes")
        else:
            print("Echec du nettoyage du fichier CSV existant")
    else:
        print("Aucun fichier CSV existant trouve. Telechargement des donnees")
        
        all_products = []
        for page in range(1, NUM_PAGES + 1):
            print(f"Telechargement page {page}/{NUM_PAGES}")
            products = fetch_products(page, PAGE_SIZE)
            if not products:
                print(f"Page {page} vide ou invalide. Passage a la suivante")
                continue
            all_products.extend([extract_product_info(p) for p in products])
            time.sleep(1)

        df = pd.DataFrame(all_products)
        print(f"{len(df)} produits extraits")

        save_to_csv(df, csv_path)
        
        # Nettoyer le fichier CSV fraichement cree
        print("Nettoyage du fichier CSV telecharge")
        cleaned_df = clean_csv_file(csv_path, cleaned_csv_path)
        if cleaned_df is None:
            print("Echec du nettoyage, utilisation du fichier original")
            cleaned_df = df
    
    # Charger dans BigQuery
    credentials_path = get_credentials_path()
    if credentials_path:
        # Utiliser le fichier nettoye s'il existe, sinon le fichier original
        file_to_load = cleaned_csv_path if os.path.exists(cleaned_csv_path) else csv_path
        load_to_bigquery(file_to_load, BQ_TABLE)
        
        try:
            bq_df = get_data_from_bigquery(BQ_TABLE)
            if not bq_df.empty:
                transformed_df = transform_data(bq_df)
                transformed_df.to_csv(transformed_csv_path, index=False)
                print(f"Donnees transformees sauvegardees : {transformed_csv_path}")
        except Exception as e:
            print(f"Erreur lors de la recuperation depuis BigQuery : {e}")
    else:
        print("Pipeline termine sans chargement BigQuery (credentials manquants)")

if __name__ == "__main__":
    # Configuration des credentials
    credentials_path = get_credentials_path()
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        print(f"Credentials configures : {credentials_path}")
    else:
        print("Attention : Impossible de trouver le fichier de credentials")
        print("Assurez-vous que le fichier de credentials est present ou configure dans config/.env")
    
    main() 