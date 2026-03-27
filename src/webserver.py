from flask import Flask, request, jsonify
from flask_cors import CORS
import src.task_repository_sqlite as repo

app = Flask(__name__)
CORS(app)


@app.get("/")
def home():
    return {
        "status": "ok",
        "endpoints": [
            "GET /tasks",
            "POST /tasks",
            "GET /tasks/<id>",
            "PUT /tasks/<id>",
            "DELETE /tasks/<id>",
            "GET /categories",
            "POST /categories",
            "GET /categories/<id>/tasks"
        ]
    }


# ------------------------------
# TASKS
# ------------------------------

@app.get("/tasks")
def get_tasks():
    return jsonify(repo.read_all())


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = repo.read(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task no encontrada"}), 404


@app.post("/tasks")
def create_task():
    data = request.json
    new_id = repo.create(data)
    return jsonify({"id": new_id}), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.json
    ok = repo.update(task_id, data)
    return jsonify({"updated": ok})


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    ok = repo.delete(task_id)
    return jsonify({"deleted": ok})


# ------------------------------
# CATEGORIES
# ------------------------------


from .task import (
    post_category,
    get_all_categories,
    get_tasks_by_category
)

@app.get("/categories")
def list_categories():
    return jsonify(get_all_categories()), 200


@app.post("/categories")
def create_category():
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "nombre requerido"}), 400

    new_id = post_category(nombre)
    return jsonify({"id": new_id, "nombre": nombre}), 201


@app.get("/categories/<int:category_id>/tasks")
def tasks_by_category(category_id):
    tasks = get_tasks_by_category(category_id)
    return jsonify(tasks), 200



# ------------------------------
# RUN
# ------------------------------

if __name__ == "__main__":
    print("Servidor en http://127.0.0.1:5000")
    app.run(debug=True)
