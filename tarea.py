# tarea.py
from datetime import datetime

class Tarea:
    def __init__(self, descripcion, fecha_vencimiento=None, completada=False):
        self.descripcion = descripcion
        self.fecha_creacion = datetime.utcnow()  # Establecer la fecha de creación en el momento actual
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%dT%H:%M:%SZ') if fecha_vencimiento else None
        self.completada = completada

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        fecha_vencimiento = self.fecha_vencimiento.strftime('%Y-%m-%d') if self.fecha_vencimiento else "No especificada"
        return f"Tarea: {self.descripcion}, Estado: {estado}, Fecha de vencimiento: {fecha_vencimiento}"