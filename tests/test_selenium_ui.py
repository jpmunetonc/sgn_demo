import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """Inicializa y configura el navegador Chrome usando WebDriver Manager."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_ui_registro_estudiante_aprobado(driver):
    """
    CP01-UI: Registro de estudiante aprobado y renderizado de detalles en la tabla.
    """
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "nombre").send_keys("Mateo Gómez")
    driver.find_element(By.ID, "n1").send_keys("4.5")
    driver.find_element(By.ID, "p1").send_keys("0.3")
    driver.find_element(By.ID, "n2").send_keys("4.0")
    driver.find_element(By.ID, "p2").send_keys("0.3")
    driver.find_element(By.ID, "n3").send_keys("3.8")
    driver.find_element(By.ID, "p3").send_keys("0.4")

    driver.find_element(By.CSS_SELECTOR, "#formEstudiante button[type='submit']").click()
    time.sleep(1)

    tabla_html = driver.find_element(By.ID, "tablaEstudiantes").text
    assert "Mateo Gómez" in tabla_html
    assert "Aprobado" in tabla_html
    assert "N1: 4.5 (30%)" in tabla_html


def test_ui_registro_estudiante_reprobado(driver):
    """
    CP02-UI: Registro de estudiante reprobado y asignación de estado.
    """
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "nombre").send_keys("Laura Pérez")
    driver.find_element(By.ID, "n1").send_keys("2.0")
    driver.find_element(By.ID, "p1").send_keys("0.3")
    driver.find_element(By.ID, "n2").send_keys("2.5")
    driver.find_element(By.ID, "p2").send_keys("0.3")
    driver.find_element(By.ID, "n3").send_keys("3.0")
    driver.find_element(By.ID, "p3").send_keys("0.4")

    driver.find_element(By.CSS_SELECTOR, "#formEstudiante button[type='submit']").click()
    time.sleep(1)

    tabla_html = driver.find_element(By.ID, "tablaEstudiantes").text
    assert "Laura Pérez" in tabla_html
    assert "Reprobado" in tabla_html


def test_ui_persistencia_recarga_pagina(driver):
    """
    CP03-UI: Verificación de recarga de datos al actualizar el navegador (F5).
    """
    driver.get("http://127.0.0.1:5000/")

    # Registrar un estudiante
    driver.find_element(By.ID, "nombre").send_keys("Camilo Ruiz")
    driver.find_element(By.ID, "n1").send_keys("4.0")
    driver.find_element(By.ID, "p1").send_keys("0.3")
    driver.find_element(By.ID, "n2").send_keys("4.0")
    driver.find_element(By.ID, "p2").send_keys("0.3")
    driver.find_element(By.ID, "n3").send_keys("4.0")
    driver.find_element(By.ID, "p3").send_keys("0.4")
    driver.find_element(By.CSS_SELECTOR, "#formEstudiante button[type='submit']").click()
    time.sleep(1)

    # Recargar la página explícitamente
    driver.refresh()
    time.sleep(1)

    # Comprobar que cargarTabla() ejecutó en la recarga y recuperó el estudiante
    tabla_html = driver.find_element(By.ID, "tablaEstudiantes").text
    assert "Camilo Ruiz" in tabla_html


def test_ui_consulta_estudiante_existente(driver):
    """
    CP04-UI: Consulta individual mediante el módulo de búsqueda.
    """
    driver.get("http://127.0.0.1:5000/")

    input_buscar = driver.find_element(By.ID, "buscarCodigo")
    input_buscar.send_keys("A1")
    driver.find_element(By.XPATH, "//button[contains(text(),'Buscar')]").click()
    time.sleep(1)

    resultado_texto = driver.find_element(By.ID, "resultadoBusqueda").text
    assert "Código: A1" in resultado_texto


def test_ui_consulta_estudiante_inexistente(driver):
    """
    CP05-UI: Consulta de un código no registrado en el sistema.
    """
    driver.get("http://127.0.0.1:5000/")

    input_buscar = driver.find_element(By.ID, "buscarCodigo")
    input_buscar.send_keys("Z99")
    driver.find_element(By.XPATH, "//button[contains(text(),'Buscar')]").click()
    time.sleep(1)

    resultado_texto = driver.find_element(By.ID, "resultadoBusqueda").text
    assert "Estudiante no encontrado" in resultado_texto


def test_ui_error_nota_fuera_de_rango(driver):
    """
    CP06-UI: Verificación de límites HTML5 max="5" en la interfaz.
    """
    driver.get("http://127.0.0.1:5000/")
    input_n1 = driver.find_element(By.ID, "n1")
    assert input_n1.get_attribute("max") == "5"


def test_ui_error_suma_pesos_invalida(driver):
    """
    CP07-UI: Renderizado de mensaje de error por suma de pesos != 1.0.
    """
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "nombre").send_keys("Ana Silva")
    driver.find_element(By.ID, "n1").send_keys("4.0")
    driver.find_element(By.ID, "p1").send_keys("0.5")
    driver.find_element(By.ID, "n2").send_keys("4.0")
    driver.find_element(By.ID, "p2").send_keys("0.5")
    driver.find_element(By.ID, "n3").send_keys("4.0")
    driver.find_element(By.ID, "p3").send_keys("0.5")

    driver.find_element(By.CSS_SELECTOR, "#formEstudiante button[type='submit']").click()
    time.sleep(1)

    error_texto = driver.find_element(By.ID, "mensajeError").text
    assert "sumar 1.0" in error_texto or "100%" in error_texto or len(error_texto) > 0


def test_ui_campos_requeridos_vacios(driver):
    """
    CP08-UI: Comprobación de obligatoriedad en los controles HTML5.
    """
    driver.get("http://127.0.0.1:5000/")
    input_nombre = driver.find_element(By.ID, "nombre")
    assert input_nombre.get_attribute("required") is not None