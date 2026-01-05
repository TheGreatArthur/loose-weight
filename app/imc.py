def calcul_imc(poids_kg: float, taille_m: float) -> float:
    """
    Calcule l'IMC à partir du poids (kg) et de la taille (m).
    """
    if poids_kg <= 0 or taille_m <= 0:
        raise ValueError("Le poids et la taille doivent être positifs")

    return round(poids_kg / (taille_m ** 2), 2)


def categorie_imc(imc: float) -> str:
    """
    Détermine la catégorie IMC.
    """
    if imc < 18.5:
        return "Insuffisance pondérale"
    elif imc < 25:
        return "Poids normal"
    elif imc < 30:
        return "Surpoids"
    else:
        return "Obésité"
