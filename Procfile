# Procfile
web: gunicorn gisele.wsgi:application
worker: celery -A gisele worker --loglevel=info
beat: celery -A gisele beat --scheduler django_celery_beat.schedulers:DatabaseScheduler