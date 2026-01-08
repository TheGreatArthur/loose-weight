import importlib
from pathlib import Path
import re

import pytest


def test_pipeline_jules(tmp_path, monkeypatch):
    """Test exécuté par la pipeline Jenkins :
    - poste les données pour l'utilisateur Jules (190 kg, 1.90 m)
    - affiche en brut les données envoyées
    - affiche le message flash renvoyé par l'application
    """

    # Isoler la base de données pour ce test
    import app.database as database
    database.DB_PATH = Path(tmp_path) / "test_imc.db"
    importlib.reload(database)
    # Initialiser explicitement la base (vide) pour éviter toute contamination
    database.init_db()

    # Importer l'application après avoir configuré DB_PATH
    import app.web as web
    importlib.reload(web)

    # Monkeypatcher la génération de PDF pour ne pas dépendre d'IO extérieurs
    def fake_generate_pdf(poids, taille, imc, categorie, output_path="rapport_imc.pdf"):
        out = Path(tmp_path) / output_path
        out.write_text("PDF stub")
        return str(out)

    monkeypatch.setattr(web, "generate_pdf", fake_generate_pdf)

    # Forcer web à utiliser la couche database isolée (tmp_path)
    # Certains imports au niveau module peuvent lier des fonctions à l'ancienne DB;
    # forcer web à appeler les fonctions du module database fraîchement rechargé.
    monkeypatch.setattr(web, "get_all_entries", database.get_all_entries)
    monkeypatch.setattr(web, "add_entry", database.add_entry)

    client = web.app.test_client()

    # Données à tester
    nom = "Jules"
    poids = "190"
    taille = "1.90"

    # Afficher les données brutes pour la pipeline
    print(f"RAW_INPUT: nom={nom}, poids={poids}, taille={taille}")

    # Poster le formulaire (inclure 'pdf' pour déclencher la génération)
    resp = client.post("/", data={"nom": nom, "poids": poids, "taille": taille, "pdf": "1"}, follow_redirects=True)
    assert resp.status_code == 200

    body = resp.get_data(as_text=True)

    # Extraire le message flash rendu dans le template (div.flash)
    m = re.search(r'<div class="flash">(.*?)</div>', body, re.S)
    message = m.group(1).strip() if m else ""

    # Afficher le message pour la pipeline (sortie standard)
    print("FLASH_MESSAGE:", message)

    # Enregistrer un petit artifact pour la pipeline contenant les valeurs
    # brutes et le message flash afin que Jenkins puisse l'archiver et l'afficher.
    out = Path.cwd() / "pipeline-output.txt"
    out.write_text(f"RAW_INPUT: nom={nom}, poids={poids}, taille={taille}\nFLASH_MESSAGE: {message}\n")

    # Le test doit renvoyer le message affiché par l'application. Selon l'état
    # de la base (déjà existante ou non) le message peut varier. On vérifie
    # simplement qu'un message est bien affiché.
    assert message != "", "Aucun message flash retourné par l'application"
