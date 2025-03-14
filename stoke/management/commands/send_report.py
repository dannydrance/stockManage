# yourapp/management/commands/send_report.py
from django.core.management.base import BaseCommand
from stoke.views import send_daily_report  # Import the function

class Command(BaseCommand):
    help = 'Send daily product report'

    def handle(self, *args, **kwargs):
        send_daily_report()
        self.stdout.write(self.style.SUCCESS('Successfully sent daily report'))