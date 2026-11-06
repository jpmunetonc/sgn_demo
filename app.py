from flask import Flask, request, jsonify, render_template
from notas import validar_nota, calcular_nota_final

app = Flask(__name__)

# Base de datos simulada en memoria y contador para autoincrementar código
estudiantes_db = {}
contador_id = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    global contador_id
    data = request.json
    
    # Autogenerar código secuencial (A1, A2, A3...)
    codigo = f"A{contador_id}"
    
    nombre = data.get("nombre")
    notas = data.get("notas")
    pesos = data.get("pesos")

    if not all([nombre, notas, pesos]):
        return jsonify({"error": "Faltan datos obligatorios (nombre, notas, pesos)"}), 400

    try:
        notas_validadas = [validar_nota(n) for n in notas]
        nota_final, estado = calcular_nota_final(notas_validadas, pesos)
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

    estudiantes_db[codigo] = {
        "codigo": codigo,
        "nombre": nombre,
        "notas": notas_validadas,
        "pesos": pesos,
        "nota_final": nota_final,
        "estado": estado
    }
    
    contador_id += 1
    return jsonify(estudiantes_db[codigo]), 201

@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    return jsonify(list(estudiantes_db.values()))

@app.route('/estudiantes/<codigo>', methods=['GET'])
def obtener_estudiante(codigo):
    estudiante = estudiantes_db.get(codigo)
    if not estudiante:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(estudiante)

if __name__ == '__main__':
    app.run(debug=True, port=5000)