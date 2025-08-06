#!/usr/bin/env python3
"""
Script de vérification des imports pour le projet OpenFoodFacts
"""

def check_imports():
    """Vérifie que tous les imports nécessaires fonctionnent"""
    print("🔍 Vérification des imports...")
    print("=" * 40)
    
    imports_to_check = [
        ("pandas", "pd"),
        ("requests", "requests"),
        ("google.cloud.bigquery", "bigquery"),
        ("google.cloud.storage", "storage"),
        ("google.auth", "auth"),
        ("numpy", "np"),
        ("os", "os"),
        ("re", "re"),
        ("time", "time")
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module, alias in imports_to_check:
        try:
            if module == "pandas":
                import pandas as pd
                print(f"✅ {module} (version {pd.__version__})")
            elif module == "requests":
                import requests
                print(f"✅ {module} (version {requests.__version__})")
            elif module == "google.cloud.bigquery":
                from google.cloud import bigquery
                print(f"✅ {module}")
            elif module == "google.cloud.storage":
                from google.cloud import storage
                print(f"✅ {module}")
            elif module == "google.auth":
                import google.auth
                print(f"✅ {module}")
            elif module == "numpy":
                import numpy as np
                print(f"✅ {module} (version {np.__version__})")
            elif module == "os":
                import os
                print(f"✅ {module}")
            elif module == "re":
                import re
                print(f"✅ {module}")
            elif module == "time":
                import time
                print(f"✅ {module}")
            
            successful_imports.append(module)
            
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"⚠️ {module}: Erreur inattendue - {e}")
            failed_imports.append(module)
    
    print("\n" + "=" * 40)
    print("📊 Résumé :")
    print(f"✅ Imports réussis : {len(successful_imports)}")
    print(f"❌ Imports échoués : {len(failed_imports)}")
    
    if failed_imports:
        print(f"\n⚠️ Packages manquants : {', '.join(failed_imports)}")
        print("\n💡 Pour installer les packages manquants :")
        print("   python install_dependencies.py")
        print("   ou")
        for package in failed_imports:
            if package == "google.cloud.bigquery":
                print("   pip install google-cloud-bigquery")
            elif package == "google.cloud.storage":
                print("   pip install google-cloud-storage")
            elif package == "google.auth":
                print("   pip install google-auth")
            else:
                print(f"   pip install {package}")
        return False
    else:
        print("\n🎉 Tous les imports sont réussis !")
        print("✅ Vous pouvez maintenant lancer le pipeline.")
        return True

if __name__ == "__main__":
    check_imports() 