from celery import Celery

celery = Celery("bookmyshow-tq", broker="redis://localhost:6379/0")
celery.conf.update(
    task_track_started=True,
    result_backend="redis://localhost:6379/0"
)