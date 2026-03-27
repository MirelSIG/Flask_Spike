from .task_repository_sqlite import (
    read,
    read_all,
    create,
    update,
    delete,
    create_category,
    list_categories,
    tasks_by_category,
)

# ------------------------------
# TASKS (ya existentes)
# ------------------------------

def get_all_tasks():
    return read_all()

def get_task_by(task_id):
    return read(task_id)

def post_task(data):
    return create(data)

def update_task(task_id, data):
    return update(task_id, data)

def del_task(task_id):
    return delete(task_id)

# ------------------------------
# CATEGORIES (nuevos)
# ------------------------------

def post_category(nombre):
    return create_category(nombre)

def get_all_categories():
    return list_categories()

def get_tasks_by_category(category_id):
    return tasks_by_category(category_id)

