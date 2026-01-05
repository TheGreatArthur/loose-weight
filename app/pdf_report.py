from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

def generate_pdf(poids, taille, imc, categorie, output_path="rapport_imc.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Rapport de suivi IMC")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Généré le : {date.today()}")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Données saisies")
    y -= 25

    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Poids : {poids} kg")
    y -= 20
    c.drawString(60, y, f"Taille : {taille} m")
    y -= 20
    c.drawString(60, y, f"IMC : {imc}")
    y -= 20
    c.drawString(60, y, f"Catégorie : {categorie}")
    y -= 40

    c.save()
    print(f"PDF généré : {output_path}")
