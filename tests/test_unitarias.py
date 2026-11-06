import pytest
from notas import validar_nota, calcular_nota_final

def test_validar_nota_correcta():
    assert validar_nota(4.0) == 4.0
    assert validar_nota(3) == 3.0

def test_validar_nota_tipo_invalido():
    with pytest.raises(TypeError):
        validar_nota("tres")
    with pytest.raises(TypeError):
        validar_nota(True)

def test_validar_nota_fuera_de_rango():
    with pytest.raises(ValueError):
        validar_nota(-0.5)
    with pytest.raises(ValueError):
        validar_nota(5.5)

def test_calcular_nota_final_aprobado():
    notas = [4.0, 3.5, 4.5]
    pesos = [0.3, 0.3, 0.4]
    nota_final, estado = calcular_nota_final(notas, pesos)
    assert nota_final == 4.05
    assert estado == "Aprobado"

def test_calcular_nota_final_reprobado():
    notas = [2.0, 2.5, 3.0]
    pesos = [0.3, 0.3, 0.4]
    nota_final, estado = calcular_nota_final(notas, pesos)
    assert nota_final == 2.55
    assert estado == "Reprobado"

def test_calcular_nota_pesos_invalidos():
    notas = [3.0, 3.0, 3.0]
    # Los pesos suman 1.2 (inválido, debe sumar 1.0)
    pesos_mal = [0.4, 0.4, 0.4]
    with pytest.raises(ValueError):
        calcular_nota_final(notas, pesos_mal)