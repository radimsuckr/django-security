from settings.celery import app as celery_app

from security.tasks import LoggedTask


@celery_app.task(
    base=LoggedTask,
    bind=True,
    name='sum_task')
def sum_task(self, task_id, a, b):
    return a + b


@celery_app.task(
    base=LoggedTask,
    bind=True,
    name='error_task')
def error_task(self, task_id):
    raise RuntimeError('error')
