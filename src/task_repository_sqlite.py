import sqlite3
from pathlib import Path

# El archivo de base de datos se guarda en la raíz del proyecto para que
# toda la aplicación use una única ubicación compartida.
DB_PATH = str(Path(__file__).resolve().parent.parent / "tasks.db")


def _init_db():
    # Se abre una conexión temporal solo para preparar el esquema.
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # SQLite no aplica claves foráneas automáticamente; esta opción las activa.
    cur.execute("PRAGMA foreign_keys = ON;")

    # Tabla principal de tareas. Si ya existe, no se vuelve a crear.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT 0,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Tabla de categorías para agrupar tareas por tema.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
        """
    )

    # Migración simple: si la tabla tasks es antigua, le agregamos category_id.
    cur.execute("PRAGMA table_info(tasks)")
    columnas = [col[1] for col in cur.fetchall()]

    if "category_id" not in columnas:
        # category_id apunta a categories.id, lo que permite relacionar ambas tablas.
        cur.execute(
            "ALTER TABLE tasks ADD COLUMN category_id INTEGER REFERENCES categories(id)"
        )

    # Guardamos cualquier cambio del esquema antes de cerrar la conexión.
    con.commit()
    con.close()


# Inicializa la base y el esquema al importar este módulo.
_init_db()


# ------------------------------
# Helpers
# ------------------------------

def _task_from_row(row):
    # Convierte una fila cruda de SQLite en un diccionario listo para JSON.
    if row is None:
        return None
    return {
        "id": row[0],
        "titulo": row[1],
        "descripcion": row[2],
        "completada": bool(row[3]),
        "fecha_creacion": row[4],
        "category_id": row[5] if len(row) > 5 else None,
    }


# ------------------------------
# CRUD TASKS
# ------------------------------

def read(task_id):
    # Devuelve una única tarea por id.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute(
            "SELECT id, titulo, descripcion, completada, fecha_creacion, category_id FROM tasks WHERE id = ?",
            (task_id,),
        )
        return _task_from_row(res.fetchone())
    finally:
        con.close()


def read_all():
    # Devuelve todas las tareas ordenadas por id para que la salida sea estable.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute(
            "SELECT id, titulo, descripcion, completada, fecha_creacion, category_id FROM tasks ORDER BY id"
        )
        return [_task_from_row(r) for r in res.fetchall()]
    finally:
        con.close()


def create(new_task):
    # Inserta una tarea nueva usando valores por defecto cuando faltan campos.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        values = (
            new_task["titulo"],
            new_task.get("descripcion", ""),
            int(bool(new_task.get("completada", False))),
            new_task.get("category_id"),
        )
        cur.execute(
            "INSERT INTO tasks (titulo, descripcion, completada, category_id) VALUES (?, ?, ?, ?)",
            values,
        )
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def update(task_id, data):
    # Actualiza una tarea existente y retorna True solo si afectó una fila.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        values = (
            data["titulo"],
            data.get("descripcion", ""),
            int(bool(data.get("completada", False))),
            data.get("category_id"),
            task_id,
        )
        cur.execute(
            "UPDATE tasks SET titulo=?, descripcion=?, completada=?, category_id=? WHERE id=?",
            values,
        )
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()


def delete(task_id):
    # Elimina una tarea por id.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()


# ------------------------------
# CRUD CATEGORIES
# ------------------------------

def create_category(nombre):
    # Crea una categoría con nombre único.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO categories (nombre) VALUES (?)", (nombre,))
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def list_categories():
    # Lista todas las categorías para poblar selectores o filtros.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute("SELECT id, nombre FROM categories ORDER BY id")
        return [{"id": r[0], "nombre": r[1]} for r in res.fetchall()]
    finally:
        con.close()


def tasks_by_category(category_id):
    # Recupera solo las tareas que pertenecen a una categoría concreta.
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute(
            """
            SELECT id, titulo, descripcion, completada, fecha_creacion, category_id
            FROM tasks WHERE category_id = ?
            """,
            (category_id,),
        )
        return [_task_from_row(r) for r in res.fetchall()]
    finally:
        con.close()
