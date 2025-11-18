import os
from celery import Celery

celery=Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

@celery.task
def test_task():
    return "Celery worker OK!"