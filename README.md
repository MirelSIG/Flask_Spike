# Flask_Spike - API de tareas

Este proyecto es una mini API REST hecha con Flask, pensada para aprender:

- Cómo funciona Flask.
- Cómo crear endpoints.
- Cómo devolver respuestas HTTP.
- Cómo usar SQLite.
- Cómo probar la API con Postman.

## 1. ¿Qué es Flask?

Flask es un microframework de Python que permite crear aplicaciones web y APIs de forma sencilla.  
Piensa en Flask como un motor que recibe peticiones y devuelve respuestas.

## 2. Instalación

# Crear entorno virtual (si no existe)
py -m venv .venv

# Activarlo
.\.venv\Scripts\Activate.ps1

# Instalar Flask
python -m pip install --upgrade pip
pip install Flask

# Verificar importación
python -c "import flask; print(flask.__version__)"

1. Asegúrate de tener Python 3 instalado.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

1. Ejecuta la aplicación:

```bash
python app.py
```

1. La API estará disponible en:

`http://localhost:5000`

## 3. Endpoints disponibles

Base URL: `http://localhost:5000`

- `GET /tasks/`
  - Lista todas las tareas.
  - Respuesta: `200`.

- `GET /tasks/<id>`
  - Obtiene una tarea por ID.
  - Respuestas: `200`, `404`.

- `POST /tasks/`
  - Crea una tarea.
  - Body requerido:

```json
{
  "title": "Mi tarea"
}
```

- Respuestas: `201`, `400`.

- `PUT /tasks/<id>`
  - Actualiza una tarea por ID.
  - Body requerido:

```json
{
  "title": "Tarea actualizada",
  "done": true
}
```

- Respuestas: `200`, `400`, `404`.

- `DELETE /tasks/<id>`
  - Elimina una tarea por ID.
  - Respuestas: `200`, `404`.

## 4. Probar la API con Postman

1. Abre Postman.
2. Crea o importa una colección.
3. Ejecuta las peticiones una por una.
4. Revisa códigos HTTP y respuestas JSON.

## 5. Base de datos

Se usa SQLite, una base de datos ligera que no necesita servidor.  
El archivo se crea automáticamente en el proyecto.

## 6. Objetivo del proyecto

Este spike sirve para aprender:

- Arquitectura API REST.
- Decoradores de Flask.
- Uso de `request` y `jsonify`.
- Respuestas HTTP.
- Pruebas con Postman.
- SQLite básico.
