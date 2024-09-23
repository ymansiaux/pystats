import requests
import sqlite3
import pandas as pd
from datetime import datetime


# Fonction pour obtenir les statistiques de téléchargement d'un package sur PyPI
def get_pypi_stats(package_name):
    url = f"https://pypistats.org/api/packages/{package_name}/recent"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Erreur lors de la récupération des données pour {package_name}")
        return {}


# Connexion à la base de données SQLite
def init_db():
    conn = sqlite3.connect("downloads_stats.db")
    cursor = conn.cursor()

    # Créer la table si elle n'existe pas encore
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS package_downloads (
            date TEXT,
            package_name TEXT,
            last_day INTEGER,
            last_week INTEGER,
            last_month INTEGER
        )
    """)
    conn.commit()
    return conn


# Enregistrement des données dans la base de données
def save_to_db(conn, package_name, stats):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO package_downloads (date, package_name, last_day, last_week, last_month)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            datetime.now().strftime("%Y-%m-%d"),
            package_name,
            stats["last_day"],
            stats["last_week"],
            stats["last_month"],
        ),
    )

    conn.commit()


# Packages à surveiller
packages = ["shiny", "streamlit", "dash"]

# Initialisation de la base de données
conn = init_db()

# Récupération et sauvegarde des statistiques pour chaque package
for package in packages:
    stats = get_pypi_stats(package)
    if stats:
        save_to_db(conn, package, stats)

# Fermeture de la connexion à la base de données
conn.close()
