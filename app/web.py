from flask import Flask, render_template, request
from app.imc import calcul_imc, categorie_imc
from app.pdf_report import generate_pdf
from app.database import init_db, add_entry, get_all_entries
from datetime import datetime

app = Flask(__name__)

# Initialiser la base de données
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    imc = None
    categorie = None
    entries = get_all_entries()

    if request.method == "POST":
        nom = request.form["nom"]
        poids = float(request.form["poids"])
        taille = float(request.form["taille"])

        imc = calcul_imc(poids, taille)
        categorie = categorie_imc(imc)

        # Enregistrer dans la base de données
        add_entry(nom, poids, taille, imc, categorie)
        
        # Si bouton "Générer PDF"
        if "pdf" in request.form:
            generate_pdf(poids, taille, imc, categorie)
        
        # Rafraîchir la liste
        entries = get_all_entries()

    return render_template("index.html", imc=imc, categorie=categorie, entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
