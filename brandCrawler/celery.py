from __future__ import absolute_import, unicode_literals
import os
from .settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandCrawler.settings')

app = Celery('celery_app',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND
             )

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
