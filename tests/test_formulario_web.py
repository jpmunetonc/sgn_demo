import pytest
from app import app

@pytest.fixture
def cliente():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_carga_y_restricciones_formulario_web(cliente):
    # 1. Simular la petición GET al frontend
    response = cliente.get('/')
    assert response.status_code == 200
    
    html = response.get_data(as_text=True)
    
    # 2. Validar existencia del formulario y botón principal
    assert '<form id="formEstudiante">' in html
    assert 'Guardar y Calcular' in html
    
    # 3. Validar campos obligatorios y tipo numérico
    assert 'id="nombre"' in html
    assert 'id="n1"' in html
    assert 'id="p1"' in html
    assert 'type="number"' in html
    assert 'required' in html
    
    # 4. Validar atributos de rango nativos HTML5 (0 a 5 para notas, 0 a 1 para pesos)
    assert 'min="0"' in html
    assert 'max="5"' in html
    assert 'max="1"' in html