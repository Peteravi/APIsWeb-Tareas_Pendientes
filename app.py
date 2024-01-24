# app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId  # Importa ObjectId desde bson
import signal
import sys
from datetime import datetime
import atexit

app = Flask(__name__)

# Configuración de la conexión a MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    client.server_info()  # Intentar obtener información del servidor
    db = client['tareas-api']
    collection = db['tareas']
    print("Conexión a MongoDB establecida con éxito.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    sys.exit(1)

@app.route('/')
def home():
    try:
        # Obtener tareas desde MongoDB
        tareas = list(collection.find({}, {'_id': 1, 'descripcion': 1, 'fecha_creacion': 1, 'fecha_vencimiento': 1, 'completada': 1}))

        # Imprimir tareas en consola (opcional)
        print("Tareas desde MongoDB:", tareas)

        return render_template('tareas.html', tareas=tareas)
    except Exception as e:
        print(f"Error al obtener tareas desde MongoDB: {e}")
        return jsonify({'error': 'Ocurrió un error al obtener las tareas'}), 500

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    try:
        # Obtener datos del formulario
        descripcion = request.form['descripcion']
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        
        # Validar datos del formulario
        if not descripcion:
            return jsonify({'error': 'La descripción es requerida'}), 400

        # Validar formato de fecha
        fecha_vencimiento_dt = None
        if fecha_vencimiento:
            try:
                fecha_vencimiento_dt = datetime.strptime(fecha_vencimiento, '%Y-%m-%dT%H:%M')
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido'}), 400

        # Crear documento de tarea
        tarea = {
            'descripcion': descripcion,
            'fecha_creacion': datetime.utcnow(),
            'fecha_vencimiento': fecha_vencimiento_dt,
            'completada': False
        }

        # Insertar tarea en MongoDB
        collection.insert_one(tarea)

        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error al agregar tarea: {e}")
        return jsonify({'error': 'Ocurrió un error al agregar la tarea'}), 500

@app.route('/eliminar_tarea', methods=['POST'])
def eliminar_tarea():
    try:
        tarea_id = request.form.get('id')
        # Validar que se proporcionó un ID antes de intentar eliminar
        if tarea_id:
            collection.delete_one({'_id': ObjectId(tarea_id)})  # Usa ObjectId para el ID de MongoDB
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error al eliminar tarea: {e}")
        return jsonify({'error': 'Ocurrió un error al eliminar la tarea'}), 500

def signal_handler(sig, frame):
    print('Saliendo de la aplicación...')
    client.close()  # Cerrar la conexión a MongoDB
    sys.exit(0)

if __name__ == '__main__':
    # Configurar el manejador de señales para una salida limpia
    signal.signal(signal.SIGINT, signal_handler)

    # Cerrar la conexión a MongoDB antes de salir
    atexit.register(lambda: client.close())

    # Añadir este bloque para cerrar la conexión al finalizar
    try:
        app.run(debug=True, port=5002, use_reloader=False)  # Cambia el puerto según sea necesario
    finally:
        client.close()  # Cerrar la conexión a MongoDB