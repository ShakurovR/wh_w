import os

from celery import Celery
from kombu import Exchange, Queue

app_name = "aligner"


celery_app = Celery(
    app_name,
    broker_url=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND"),
)
celery_app.conf.update(task_track_started=True, broker_connection_retry_on_startup=True)

celery_app.conf.task_queues = [
    Queue(app_name, exchange=Exchange(app_name, type="direct"), routing_key=app_name)
]

celery_app.conf.task_default_queue = app_name
celery_app.conf.task_default_exchange = app_name
celery_app.conf.task_default_routing_key = app_name
