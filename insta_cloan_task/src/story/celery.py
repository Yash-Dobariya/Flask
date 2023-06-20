from celery import Celery
from src.story.model import Story

celery_app = Celery(
    "celery_app", broker_url="amqp://myuser:mypassword@localhost:5672/myvhost"
)

@celery_app.task()
def delete_story(a):
    return a
