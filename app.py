from flask import Flask
from flask_cors import CORS
from routes.tasks import tasks_bp   # Asegúrate que esta ruta sea correcta

app = Flask(__name__)

# Habilitar CORS (útil para Postman y futuras frontends)
CORS(app)

# Registrar el Blueprint
app.register_blueprint(tasks_bp)

@app.route('/')
def home():
    return {
        "mensaje": " Backend Flask + SQLite listo ",
        "status": "ok",
        "endpoints_disponibles": [
            "GET /tasks",
            "POST /tasks",
            "GET /tasks/<id>"
        ]
    }

if __name__ == "__main__":
    # Crear la base de datos y tablas la primera vez
    from config import init_db   
    init_db()
    
    print("Servidor corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)