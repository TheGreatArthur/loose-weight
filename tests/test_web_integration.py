import importlib
from pathlib import Path

import pytest


def test_web_imc_and_pdf(tmp_path, monkeypatch):
    # Isoler la base de données dans tmp_path
    import app.database as database

    database.DB_PATH = Path(tmp_path) / "test_imc.db"
    importlib.reload(database)

    # Importer l'application Flask après avoir configuré DB_PATH
    import app.web as web
    importlib.reload(web)

    # Monkeypatcher la génération de PDF pour ne pas dépendre du filesystem global
    pdf_filename = "rapport_imc_TestJules.pdf"

    called = {}

    def fake_generate_pdf(poids, taille, imc, categorie, output_path="rapport_imc.pdf"):
        called['args'] = (poids, taille, imc, categorie, output_path)
        out = Path(tmp_path) / output_path
        out.write_text("PDF stub")
        return str(out)

    # web module importe generate_pdf au niveau du module, on le monkeypatch là
    monkeypatch.setattr(web, "generate_pdf", fake_generate_pdf)

    client = web.app.test_client()

    # GET page d'accueil
    r = client.get("/")
    assert r.status_code == 200

    # Poster le formulaire avec l'utilisateur demandé
    form = {
        "nom": "TestJules",
        "poids": "150",
        "taille": "1.90",
        # inclure une clé 'pdf' pour déclencher la génération
        "pdf": "1",
    }

    r = client.post("/", data=form, follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True)

    # Vérifier l'IMC et la catégorie affichées
    assert "41.55" in body
    assert "Obésité" in body

    # Vérifier que generate_pdf a été appelé et que le fichier stub existe
    assert 'args' in called
    output_path = Path(tmp_path) / called['args'][4]
    assert output_path.exists()

    # Vérifier que l'entrée a bien été insérée en base
    entries = web.get_all_entries()
    assert any(e['nom'] == 'TestJules' and abs(e['imc'] - 41.55) < 0.01 for e in entries)
