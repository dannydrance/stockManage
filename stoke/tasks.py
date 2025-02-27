from celery import shared_task
from .views import send_daily_report

@shared_task
def send_daily_email():
    send_daily_report()