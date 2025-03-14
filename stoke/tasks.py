from django_q.tasks import schedule
from stoke.views import send_daily_report

def send_daily_report_task():
    send_daily_report()