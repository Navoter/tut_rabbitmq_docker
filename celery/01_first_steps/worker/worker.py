#!/usr/bin/env python
import os
import time
from celery import Celery

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'mypassword')

broker_url = f'pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/{RABBITMQ_VHOST}'
result_backend = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379/0'

app = Celery('tasks', broker=broker_url, backend=result_backend)

# Konfiguriert, dass Ergebnisse nach 60 Sekunden gelöscht werden
app.conf.update(
    result_expires=60,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Berlin',
    enable_utc=False,
)

@app.task
def add(x, y):
    time.sleep(10)
    return x + y