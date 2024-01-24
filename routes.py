# routes.py
from flask import Flask, jsonify, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from tarea import Tarea

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/tareasdb'
mongo = PyMongo(app)

# Obtener todas las tareas
@app.route('/tareas', methods=['GET'])
def obtener_todas_las_tareas():
    tareas = list(mongo.db.tareas.find())
    return jsonify({'tareas': tareas})

# Crear una nueva tarea
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    tarea_data = {
        'descripcion': request.form['descripcion'],
        'fecha_vencimiento': request.form.get('fecha_vencimiento', None),  # Asegurarse de manejar la fecha correctamente
        'completada': False  # Puedes ajustar esto según tus necesidades
    }
    tarea_id = mongo.db.tareas.insert_one(tarea_data).inserted_id
    return redirect(url_for('obtener_todas_las_tareas'))

# Eliminar una tarea por ID
@app.route('/eliminar_tarea/<id>', methods=['POST'])
def eliminar_tarea(id):
    mongo.db.tareas.delete_one({'_id': id})
    return redirect(url_for('obtener_todas_las_tareas'))