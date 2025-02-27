from celery.schedules import crontab
from gisele.celery import app
from stoke.views import send_daily_report

@app.task
def send_daily_email_task():
    send_daily_report()

app.conf.beat_schedule = {
    'send-daily-email-every-morning': {
        'task': 'stoke.tasks.send_daily_email_task',
        'schedule': crontab(hour=0, minute=15),
    },
}
