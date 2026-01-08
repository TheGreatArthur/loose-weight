from flask import Flask, render_template, request, flash
from app.imc import calcul_imc, categorie_imc
from app.pdf_report import generate_pdf
from app.database import init_db, add_entry, get_all_entries
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret-key"


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

        # Récupérer l'entrée la plus récente pour cet utilisateur (avant insertion)
        previous_entry = None
        for e in entries:
            if e.get('nom') == nom:
                previous_entry = e
                break

        # Enregistrer la nouvelle entrée
        add_entry(nom, poids, taille, imc, categorie)

        # Message bienveillant selon la variation de poids
        if previous_entry is None:
            flash("Entrée enregistrée — bon début ! Continuez à suivre vos progrès 😊")
        else:
            prev_poids = float(previous_entry.get('poids', 0))
            diff = round(poids - prev_poids, 2)
            if diff < 0:
                lost = abs(diff)
                flash(f"Bravo — vous avez perdu {lost} kg depuis la dernière saisie. Continuez comme ça ! 🎉")
            elif diff > 0:
                flash(f"Courage — vous avez pris {diff} kg depuis la dernière saisie. Ne vous découragez pas, chaque jour est une nouvelle opportunité 💪")
            else:
                flash("Poids inchangé depuis la dernière saisie. Continuez vos efforts !")

        if "pdf" in request.form:
            generate_pdf(poids, taille, imc, categorie)

        # Rafraîchir la liste après insertion
        entries = get_all_entries()

    return render_template("index.html", imc=imc, categorie=categorie, entries=entries)

if __name__ == "__main__":
    app.run(debug=True)

