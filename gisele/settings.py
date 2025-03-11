"""
Django settings for gisele project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7u!*2kzmw&zu60st*s__gu@88-pxihvurac00#2s8!qeonltm6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition
#'django_extensions', python manage.py graph_models -a -o myapp_models.png
INSTALLED_APPS = [
    'jazzmin',
    "channels",
    'django_celery_results',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "stoke",
    'django_celery_beat',
    'crispy_forms',
]

ASGI_APPLICATION = "gisele.asgi.application"

JAZZMIN_SETTINGS = {
    "site_title": "My Admin",
    "site_header": "Stock Manager Admin Panel",
    "site_brand": "Stock Manager",
    "welcome_sign": "Welcome to the Admin Panel!",
    "copyright": "Stock Manager",
    # More customization options available
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("red-cv08qkq3esus73e6kghg", 6379)],  # Replace with your Redis host and port  
        },
    },
}

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gisele.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gisele.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Directory where static files will be collected during production (for use with `collectstatic`)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production use only

# Additional directories to look for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Assuming you have a 'static' directory where your app's static files are located
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lilianekamaliza790@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'aknk gued ijva aeeo'  # Gmail App Password (explained below)
#DEFAULT_FROM_EMAIL = 'hakizayezudaniel@gmail.com'

# settings.py
# Celery Configuration   redis://default:oZzVBmTxKaySOJmqbXcguPfrtIWobHtN@shuttle.proxy.rlwy.net:25096
#CELERY_BROKER_URL = 'redis://red-cv08qkq3esus73e6kghg:6379'  # Use Redis as a message broker

# Celery Configuration Options
CELERY_TIMEZONE = "Africa/Kigali"
CELERY_TASK_TRACK_STARTED = True


CELERY_BROKER_URL = 'redis://red-cv08qkq3esus73e6kghg:6379/0'  # Redis broker URL from Render
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'  # Same Redis instance for results

'''CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Or another broker like RabbitMQ
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Or another result backend if needed
CELERY_TIMEZONE = 'UTC'  # Or your desired timezone
'''
CRISPY_TEMPLATE_PACK = 'bootstrap5'  # Or 'bootstrap4'
