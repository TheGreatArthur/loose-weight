import pytest
from app.imc import calcul_imc, categorie_imc


def test_calcul_imc_valide():
    imc = calcul_imc(70, 1.75)
    assert imc == 22.86


def test_categorie_imc_normal():
    assert categorie_imc(22) == "Poids normal"


def test_categorie_imc_insuffisance():
    assert categorie_imc(17) == "Insuffisance pondérale"


def test_categorie_imc_surpoids():
    assert categorie_imc(27) == "Surpoids"


def test_categorie_imc_obesite():
    assert categorie_imc(32) == "Obésité"


def test_calcul_imc_erreur():
    with pytest.raises(ValueError):
        calcul_imc(0, 1.75)
