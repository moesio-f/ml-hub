"""Esse módulo contém a configuração do 
Celery app.
"""
import os

from celery import Celery
from kombu import Queue

app = Celery(
    'training',
    backend=os.environ['CELERY_RESULT_BACKEND'],
    broker=os.environ['CELERY_BROKER_URL'],
)

app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
app.conf.task_default_priority = 5
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize', 'pickle']

app.conf.task_queues = {
    Queue(
        'training.queue',
        exchange='training.queue',
        routing_key='training.*',
    )
}

app.conf.task_routes = {
    'training.*': {
        'queue': 'training.queue',
        'exchange': 'training.queue',
    }
}

app.conf.update(
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1
)

app.autodiscover_tasks(packages=['worker'])

