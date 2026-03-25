import sqlite3

DB_PATH = "tasks.db"


def _init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
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
    con.commit()
    con.close()


_init_db()


def _task_from_row(row):
    if row is None:
        return None
    return {
        "id": row[0],
        "titulo": row[1],
        "descripcion": row[2],
        "completada": bool(row[3]),
        "fecha_creacion": row[4],
    }


def read(task_id):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute(
            "SELECT id, titulo, descripcion, completada, fecha_creacion FROM tasks WHERE id = ?",
            (task_id,),
        )
        task_sql = res.fetchone()
        return _task_from_row(task_sql)
    except sqlite3.Error:
        return None
    finally:
        con.close()


def read_all():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute(
            "SELECT id, titulo, descripcion, completada, fecha_creacion FROM tasks ORDER BY id"
        )
        rows = res.fetchall()
        tasks = []
        for row in rows:
            tasks.append(_task_from_row(row))
        return tasks
    except sqlite3.Error:
        return []
    finally:
        con.close()


def create(new_task):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        values = (
            new_task["titulo"],
            new_task.get("descripcion", ""),
            int(bool(new_task.get("completada", False))),
        )
        cur.execute(
            "INSERT INTO tasks (titulo, descripcion, completada) VALUES (?, ?, ?)",
            values,
        )
        con.commit()
        return cur.lastrowid
    except sqlite3.Error:
        return None
    finally:
        con.close()


def update(task_id, update_task_data):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        values = (
            update_task_data["titulo"],
            update_task_data.get("descripcion", ""),
            int(bool(update_task_data.get("completada", False))),
            task_id,
        )
        cur.execute(
            "UPDATE tasks SET titulo = ?, descripcion = ?, completada = ? WHERE id = ?",
            values,
        )
        con.commit()
        return cur.rowcount > 0
    except sqlite3.Error:
        return False
    finally:
        con.close()


def delete(task_id):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        con.commit()
        return cur.rowcount > 0
    except sqlite3.Error:
        return False
    finally:
        con.close()
