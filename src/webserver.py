from flask import Flask, jsonify, request
from flask_cors import CORS

from .task import del_task, get_all_tasks, get_task_by, post_task, update_task

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def hello_root():
    return "<h1>Hola, este es el endpoint raiz de Flask_Spike</h1>"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks()), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by(task_id)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task), 200


@app.route("/tasks", methods=["POST"])
def new_task():
    data = request.get_json(silent=True) or {}
    if not data.get("titulo"):
        return jsonify({"error": "El titulo es obligatorio"}), 400

    task_id = post_task(data)
    if task_id is None:
        return jsonify({"error": "No se pudo crear la tarea"}), 500

    return jsonify({"message": "Tarea creada", "id": task_id}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    data = request.get_json(silent=True) or {}
    if not data.get("titulo"):
        return jsonify({"error": "El titulo es obligatorio"}), 400

    updated = update_task(task_id, data)
    if not updated:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify({"message": "Tarea actualizada"}), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = del_task(task_id)
    if not deleted:
        return jsonify({"error": "Tarea eliminada exitosamente"}), 404
    return "", 204
