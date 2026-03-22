from flask import Blueprint, request, jsonify
from models.task_model import (
    get_all_tasks, get_task, create_task, update_task, delete_task
)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.get("/")
def list_tasks():
    return jsonify(get_all_tasks()), 200

@tasks_bp.get("/<int:id>")
def retrieve_task(id):
    task = get_task(id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@tasks_bp.post("/")
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400

    new_id = create_task(data["title"])
    return jsonify({"message": "Task created", "id": new_id}), 201

@tasks_bp.put("/<int:id>")
def edit_task(id):
    data = request.get_json()
    if not data or "title" not in data or "done" not in data:
        return jsonify({"error": "Missing fields"}), 400

    updated = update_task(id, data["title"], data["done"])
    if updated:
        return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found"}), 404

@tasks_bp.delete("/<int:id>")
def remove_task(id):
    deleted = delete_task(id)
    if deleted:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404