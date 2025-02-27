from celery import Celery

app = Celery('gisele')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def send_daily_email_task():
    from stoke.views import send_daily_report
    send_daily_report()
