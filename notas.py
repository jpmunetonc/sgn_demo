"""Modulo de reglas de negocio: Sistema de Gestion de Notas (SGN)."""

NOTA_MIN, NOTA_MAX, NOTA_APROBATORIA = 0.0, 5.0, 3.5

def validar_nota(nota):
    if not isinstance(nota, (int, float)) or isinstance(nota, bool):
        raise TypeError("La nota debe ser numérica")
    if nota < NOTA_MIN or nota > NOTA_MAX:
        raise ValueError(f"La nota debe estar entre {NOTA_MIN} y {NOTA_MAX}")
    return float(nota)

def calcular_nota_final(notas, pesos):
    if len(notas) != len(pesos):
        raise ValueError("La cantidad de notas y pesos debe ser igual")
    
    suma_pesos = sum(pesos)
    if abs(suma_pesos - 1.0) > 1e-5:
        raise ValueError("La suma de los porcentajes (pesos) debe ser 1.0 (100%)")
    
    nota_final = sum(n * p for n, p in zip(notas, pesos))
    estado = "Aprobado" if nota_final >= NOTA_APROBATORIA else "Reprobado"
    return round(nota_final, 2), estado