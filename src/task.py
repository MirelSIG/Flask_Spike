from .task_repository_sqlite import create, delete, read, read_all, update


def get_task_by(task_id):
    return read(task_id)


def get_all_tasks():
    return read_all()


def post_task(new_task):
    return create(new_task)


def update_task(task_id, update_task_data):
    return update(task_id, update_task_data)


def del_task(task_id):
    return delete(task_id)
