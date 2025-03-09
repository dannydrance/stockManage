import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gisele.settings')

app = Celery('gisele')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

#from stoke.tasks import send_daily_email
from django.utils import timezone


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from celery.schedules import crontab

app.conf.beat_schedule = {
    'send_daily_email_task': {
        'task': 'stoke.tasks.send_daily_email',
        'schedule': crontab(minute=0, hour=8),  # Sends the email every day at 8 AM
    },
}
