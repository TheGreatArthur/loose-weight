import sqlite3
from datetime import datetime
from pathlib import Path

# Chemin de la base de données
DB_PATH = Path(__file__).parent.parent / "imc_data.db"

def get_connection():
    """Obtient une connexion à la base de données."""
    return sqlite3.connect(str(DB_PATH))

def init_db():
    """Initialise la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Créer la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            poids FLOAT NOT NULL,
            taille FLOAT NOT NULL,
            imc FLOAT NOT NULL,
            categorie_imc VARCHAR(50) NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def add_entry(nom, poids, taille, imc, categorie):
    """Ajoute une nouvelle entrée à la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    # Vérifier si un enregistrement existe déjà pour ce nom (la plus récente)
    cursor.execute(
        """
        SELECT id FROM weight_logs WHERE nom = ? ORDER BY date DESC LIMIT 1
        """,
        (nom,)
    )
    row = cursor.fetchone()

    updated = False
    if row:
        # Mettre à jour l'entrée existante
        entry_id = row[0]
        cursor.execute(
            """
            UPDATE weight_logs
            SET date = ?, poids = ?, taille = ?, imc = ?, categorie_imc = ?
            WHERE id = ?
            """,
            (today, poids, taille, imc, categorie, entry_id)
        )
        updated = True
    else:
        # Insérer une nouvelle entrée si aucun nom existant
        cursor.execute("""
            INSERT INTO weight_logs (nom, date, poids, taille, imc, categorie_imc)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, today, poids, taille, imc, categorie))

    conn.commit()
    conn.close()

    # Retourner True si on a mis à jour une entrée existante, sinon False
    return updated
    
    conn.commit()
    conn.close()

def get_all_entries():
    """Récupère toutes les entrées de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nom, date, poids, taille, imc, categorie_imc
        FROM weight_logs
        ORDER BY date DESC
    """)
    
    entries = []
    for row in cursor.fetchall():
        entries.append({
            'id': row[0],
            'nom': row[1],
            'date': row[2],
            'poids': row[3],
            'taille': row[4],
            'imc': row[5],
            'categorie_imc': row[6]
        })
    
    conn.close()
    return entries

def delete_entry(entry_id):
    """Supprime une entrée de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM weight_logs WHERE id = ?", (entry_id,))
    
    conn.commit()
    conn.close()
