import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d2ga.settings")
app = Celery("d2ga")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']
app.autodiscover_tasks()
