# Arquitectura y flujo de Flask_Spike

## Objetivo

Replicar el estilo de arquitectura de proyecto_flask_2 manteniendo el dominio de tareas.

## Capas del proyecto

1. Entrada
- app.py

2. Capa HTTP
- src/webserver.py

3. Capa de servicio
- src/task.py

4. Capa de repositorio SQLite
- src/task_repository_sqlite.py

## Responsabilidad por archivo

### app.py

- Importa app desde src/webserver.py.
- Ejecuta el servidor Flask en puerto 5000.

### src/webserver.py

- Crea la instancia Flask y habilita CORS.
- Define endpoints REST de tareas.
- Valida entrada JSON para POST y PUT.

Endpoints:

- GET /
- GET /tasks
- GET /tasks/<id>
- POST /tasks
- PUT /tasks/<id>
- DELETE /tasks/<id>

### src/task.py

- Encapsula la logica de negocio minima.
- Expone funciones get, create, update y delete.
- Delega persistencia en el repositorio.

### src/task_repository_sqlite.py

- Inicializa automaticamente la tabla tasks si no existe.
- Ejecuta SQL con sqlite3.
- Convierte filas a diccionarios listos para jsonify.

Esquema tasks:

- id INTEGER PRIMARY KEY AUTOINCREMENT
- titulo TEXT NOT NULL
- descripcion TEXT
- completada BOOLEAN DEFAULT 0
- fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP

## Flujo de una request

Ejemplo POST /tasks:

1. Cliente envia JSON.
2. src/webserver.py valida titulo.
3. src/task.py delega a src/task_repository_sqlite.py.
4. Se ejecuta INSERT en SQLite.
5. Se responde 201 con id creado.

Ejemplo DELETE /tasks/<id>:

1. Cliente envia id.
2. webserver llama del_task.
3. repositorio ejecuta DELETE.
4. Devuelve 204 si borra o 404 si no existe.

## Flujo de inicio

1. python app.py
2. app.py importa src/webserver.py
3. webserver importa task y task_repository_sqlite
4. task_repository_sqlite crea tabla si no existe
5. Flask queda listo para recibir requests

## Dependencias

- Flask==3.0.0
- Flask-Cors==5.0.0

## Observacion operativa

Se recomienda ejecutar siempre con .venv activo para evitar errores de importacion.

## Operacion de limpieza de DDBB

La limpieza de datos en este proyecto significa:

1. Vaciar la tabla tasks.
2. Reiniciar el autoincrement para que el siguiente id vuelva a empezar en 1.

Comando de limpieza:

```bash
cd /Users/mirelvolcan/Flask_Spike
source .venv/bin/activate
python -c "import sqlite3; con=sqlite3.connect('tasks.db'); cur=con.cursor(); cur.execute('DELETE FROM tasks'); cur.execute(\"DELETE FROM sqlite_sequence WHERE name='tasks'\"); con.commit(); con.close()"
```

Validacion funcional:

```bash
python -c "from app import app; c=app.test_client(); r=c.get('/tasks'); print(r.status_code, r.get_json())"
```

Resultado esperado:

- 200 []
