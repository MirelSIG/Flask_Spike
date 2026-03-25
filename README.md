# Flask_Spike - API de tareas con Flask + SQLite

Siguiendo el patron de proyecto_flask_2:

- app.py como punto de arranque.
- src/webserver.py para rutas HTTP.
- src/task.py como capa servicio.
- src/task_repository_sqlite.py como repositorio SQLite.

## Estructura

```text
Flask_Spike/
├── app.py
├── requirements.txt
├── tasks.db
├── Flask_Spike.postman_collection.json
└── src/
    ├── __init__.py
    ├── webserver.py
    ├── task.py
    └── task_repository_sqlite.py
```

## Instalacion

```bash
cd /Users/mirelvolcan/Flask_Spike
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecucion

```bash
python app.py
```

Servidor local:

- http://127.0.0.1:5000

## Endpoints

Base URL: http://127.0.0.1:5000

1. GET /
2. GET /tasks
3. GET /tasks/<id>
4. POST /tasks
5. PUT /tasks/<id>
6. DELETE /tasks/<id>

Body ejemplo para POST y PUT:

```json
{
  "titulo": "Mi tarea",
  "descripcion": "Detalle opcional",
  "completada": false
}
```

## Base de datos

La tabla tasks se crea automaticamente desde src/task_repository_sqlite.py.

Campos:

- id INTEGER PRIMARY KEY AUTOINCREMENT
- titulo TEXT NOT NULL
- descripcion TEXT
- completada BOOLEAN DEFAULT 0
- fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP

### Limpiar DDBB (reset)

Para vaciar la tabla y reiniciar el contador de ids:

```bash
cd /Users/mirelvolcan/Flask_Spike
source .venv/bin/activate
python -c "import sqlite3; con=sqlite3.connect('tasks.db'); cur=con.cursor(); cur.execute('DELETE FROM tasks'); cur.execute(\"DELETE FROM sqlite_sequence WHERE name='tasks'\"); con.commit(); con.close()"
```

Comprobar que quedo vacia:

```bash
python -c "from app import app; c=app.test_client(); r=c.get('/tasks'); print(r.status_code, r.get_json())"
```

Salida esperada:

- 200 []

## Nota

Si usas python3 global puede fallar por dependencias fuera del entorno virtual.
Usa siempre .venv activado para ejecutar el backend.
