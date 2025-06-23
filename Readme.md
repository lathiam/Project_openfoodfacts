# Projet ETL OpenFoodFacts

## 📋 Description

Ce projet met en place un pipeline ETL (Extract, Transform, Load) pour collecter, transformer et analyser les données de l'API OpenFoodFacts.

## 🎯 Objectifs

- **Collecte** : Récupération des données via l'API OpenFoodFacts
- **Transformation** : Nettoyage et structuration des données collectées
- **Stockage** : Sauvegarde des données dans BigQuery
- **Analyse** : Génération d'insights et de rapports

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Extraction    │───▶│  Transformation │───▶│     Loading     │───▶│    Analyse      │
│  (API Calls)    │    │  (Data Cleaning)│    │   (BigQuery)    │    │   (Reports)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```




2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```



## 📊 Technologies Utilisées

- **Python** : Langage principal
- **BigQuery** : Base de données cloud
- **OpenFoodFacts API** : Source de données
- **Pandas** : Manipulation des données
-