from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

tasks_bp = Blueprint('tasks', __name__)

# GET ALL 
@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "completada": bool(row[3]),
            "fecha_creacion": row[4]
        })
    
    return jsonify(tasks)

# ==================== CREATE ====================
@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    titulo = data.get('titulo')
    descripcion = data.get('descripcion', '')

    if not titulo:
        return jsonify({"error": "El título es obligatorio"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (titulo, descripcion)
        VALUES (?, ?)
    ''', (titulo, descripcion))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "mensaje": "Tarea creada exitosamente",
        "id": task_id,
        "titulo": titulo
    }), 201