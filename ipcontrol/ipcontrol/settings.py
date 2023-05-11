from pathlib import Path
from django.contrib.messages import constants
import os
from datetime import date
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
TODAY=date.today()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY= env.str('DJANGO_SECRET_KEY', default='django-insecure-7*q!s1mxb(fw*_6+9k$=e63#e#alke^bp5kq8^8j#s^t*yith&')

DEBUG = env.bool('DEBUG', default=False) #os.environ.get('DJANGO_DEBUG', '') != 'False'


# ALLOWED_HOSTS = ['127.0.0.1','192.168.189.250']
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
LOG_FILE_PATH = os.path.join(env.str('LOG_FILE_PATH'), TODAY.strftime("%d-%m-%Y"))
# Tempo de vida do COOKIE
SESSION_COOKIE_AGE = 10800
SESSION_SAVE_EVERY_REQUEST = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'maccontrol'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ipcontrol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'filter': 'store.templatetags.filter'
            }
        },
    },
]

WSGI_APPLICATION = 'ipcontrol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    constants.DEBUG : 'alert-primary',
    constants.ERROR : 'alert-danger',
    constants.SUCCESS : 'alert-success',
    constants.INFO : 'alert-info',
    constants.WARNING : 'alert-warning',
}


# Logs
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            # "verbose": {
            #     "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            #     "style": "{",
            # },
            "simple": {
                "format": "{levelname}:{asctime}:{module}:{message}",
                "style": "{",
            },
        }, #warning
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": f"{LOG_FILE_PATH}.log",
                "formatter":"simple"
            },
            "file2":{
                "level": "WARNING",
                "class": "logging.FileHandler",
                "filename": f"{LOG_FILE_PATH}_django.log",
                "formatter":"simple"
            }
        },
        "loggers": {
            "djangojr": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": False,
            },
            "django":{
                "handlers": ["file2"],
                "level": "WARNING",
                "propagate": False,
            }
        },
    }