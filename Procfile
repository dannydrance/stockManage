# Procfile
web: gunicorn gisele.wsgi:application
worker: celery -A gisele worker --loglevel=info
beat: celery -A gisele beat --loglevel=info