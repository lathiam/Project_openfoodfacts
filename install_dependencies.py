#!/usr/bin/env python3
"""
Script d'installation des dépendances pour le projet OpenFoodFacts
"""

import subprocess
import sys
import os

def install_package(package):
    """Installe un package avec pip"""
    try:
        print(f"🔄 Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation de {package}: {e}")
        return False

def main():
    """Fonction principale d'installation"""
    print("🚀 Installation des dépendances pour le projet OpenFoodFacts")
    print("=" * 60)
    
    # Liste des packages essentiels
    essential_packages = [
        "pandas",
        "requests",
        "google-cloud-bigquery",
        "google-cloud-storage",
        "google-auth",
        "numpy",
        "db-dtypes"  # Ajout du package manquant
    ]
    
    # Liste des packages optionnels
    optional_packages = [
        "jupyter",
        "matplotlib",
        "seaborn"
    ]
    
    print("📦 Installation des packages essentiels...")
    failed_packages = []
    
    for package in essential_packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Packages échoués : {', '.join(failed_packages)}")
        print("💡 Essayez d'installer manuellement ces packages :")
        for package in failed_packages:
            print(f"   pip install {package}")
    else:
        print("\n✅ Tous les packages essentiels installés avec succès !")
    
    # Demander pour les packages optionnels
    print(f"\n📦 Packages optionnels disponibles : {', '.join(optional_packages)}")
    response = input("Voulez-vous installer les packages optionnels ? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', 'oui', 'o']:
        print("\n📦 Installation des packages optionnels...")
        for package in optional_packages:
            install_package(package)
    
    print("\n🎉 Installation terminée !")
    print("\n📋 Prochaines étapes :")
    print("1. Vérifiez que tout fonctionne : python test_pipeline.py")
    print("2. Nettoyez le CSV existant : python clean_csv.py")
    print("3. Lancez le pipeline : python openfoodfacts_pipeline.py")

if __name__ == "__main__":
    main() 