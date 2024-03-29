from pathlib import Path
import decouple 
from celery.schedules import crontab

import environ

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c&h53n+8a!65s$vck_5yf1*yi)1mdet7jg5$4pi3tu^@#748o!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'alertApp',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pricealertproject.urls"

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

WSGI_APPLICATION = "pricealertproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # "NAME": BASE_DIR / "db.sqlite3",
        'NAME': env.str('MYSQL_DATABASE','alertsystem'),
        
        # 'NAME': 'alertsystem',
        'USER': env.str('MYSQL_USER','alert'),
        # 'USER': 'root',
        'PASSWORD': env.str('MYSQL_PASSWORD','password'),
        # 'PASSWORD': 'password',
        'HOST': env.str('DB_HOST', 'localhost'),  # Use 'db' as default from .env
        # 'HOST': 'localhost',
        'PORT': env.str('DB_PORT', '3306'),  # Use '3306' as default from .env
        # 'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.str("REDIS_URL", "redis://localhost:6379/"),
        "KEY_PREFIX": "alersystem",
        # "OPTIONS": {
        #      "PASSWORD": "jaqc31l",
        #      "CLIENT_CLASS": "django.core.cache.backends.redis.DefaultClient",
        # },
        "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
    }
}

CACHE_TTL = 60 * 15

CELERY_BROKER_URL = env.str("REDIS_URL", "redis://localhost:6379/")
CELERY_RESULT_BACKEND = env.str("REDIS_URL", "redis://localhost:6379/")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULE = {
'task-number-one': {
'task': 'jobs.tasks.sendAlert',
'schedule': crontab(minute='*/1')
}
}
