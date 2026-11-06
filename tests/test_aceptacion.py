import pytest
from app import app, estudiantes_db
import app as modulo_app  # Importamos el módulo para resetear el contador

@pytest.fixture
def cliente():
    app.config['TESTING'] = True
    estudiantes_db.clear()
    modulo_app.contador_id = 1  # Reiniciamos el contador de códigos a A1 en cada test
    with app.test_client() as client:
        yield client

def test_crear_y_consultar_estudiante_aprobado(cliente):
    # Petición POST
    response = cliente.post('/estudiantes', json={
        "nombre": "Laura",
        "notas": [4.0, 4.5, 4.0],
        "pesos": [0.3, 0.3, 0.4]
    })
    assert response.status_code == 201
    data_creada = response.get_json()
    assert data_creada["codigo"] == "A1"
    assert data_creada["estado"] == "Aprobado"

    # Petición GET para consultar un estudiante específico
    get_response = cliente.get('/estudiantes/A1')
    assert get_response.status_code == 200
    estudiante = get_response.get_json()
    assert estudiante["nombre"] == "Laura"
    assert estudiante["nota_final"] == 4.15

def test_listar_todos_los_estudiantes(cliente):
    # Registrar dos estudiantes para probar el GET general
    cliente.post('/estudiantes', json={"nombre": "Carlos", "notas": [3.0, 3.0, 3.0], "pesos": [0.3, 0.3, 0.4]})
    cliente.post('/estudiantes', json={"nombre": "Ana", "notas": [5.0, 4.8, 4.9], "pesos": [0.3, 0.3, 0.4]})
    
    # Petición GET general (Tabla general)
    response = cliente.get('/estudiantes')
    assert response.status_code == 200
    lista = response.get_json()
    assert len(lista) == 2
    assert lista[0]["codigo"] == "A1"
    assert lista[1]["codigo"] == "A2"

def test_consultar_estudiante_inexistente(cliente):
    response = cliente.get('/estudiantes/Z99')
    assert response.status_code == 404
    assert response.get_json()["error"] == "No encontrado"

def test_crear_estudiante_nota_fuera_de_rango(cliente):
    response = cliente.post('/estudiantes', json={
        "nombre": "Pedro",
        "notas": [6.0, 3.0, 3.0],
        "pesos": [0.3, 0.3, 0.4]
    })
    assert response.status_code == 400
    assert "error" in response.get_json()