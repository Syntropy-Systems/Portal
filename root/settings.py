"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .local_settings import *
# from cloghandler import ConcurrentRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ew*32x_+=b-g=4g%)111o2isb+)zn(^$6b#wtq_geuf9fy8@jocc%='
PRECISION = 2
DESIGN_STATE = 1 #1 for default and 2 for inspinia

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'mail_templated',
    'rest_framework',
    'rest_framework.authtoken',
    'project',
    'apiv1',
]


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'project.middleware.user_middleware.User_middleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTH_USER_MODEL = 'project.User'
WSGI_APPLICATION = 'root.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


"""Make a file called 'local_settings.py' in the same folder as 'settings.py' and have this as its contents:
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST' : host,
        'PORT' : '',
    }
}
# env = None





# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'weprobpo.market@gmail.com'
EMAIL_HOST_PASSWORD = 'prqzzbdluagxcmnu'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/static/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'project/static/uploads')


ERROR_LEVEL = 'WARNING' # DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
CORS_ORIGIN_ALLOW_ALL = True




ENVIRONMENT = env
DEBUG = True
ALLOWED_HOSTS = []

if ENVIRONMENT == "production":
    DEBUG = False
    ALLOWED_HOSTS = ["*"]

    STATIC_URL = '/static_cdn/'
    STATIC_ROOT = "/home/dev/static_cdn"

    MEDIA_URL = '/media/'
    MEDIA_ROOT = "/home/dev/static_cdn/uploads"
    
else:
    # INSTALLED_APPS += ["debug_toolbar","debug_panel",]
    # MIDDLEWARE_CLASSES += ('debug_panel.middleware.DebugPanelMiddleware',)
    INTERNAL_IPS = ('localhost','127.0.0.1','127.0.0.1:8000','127.0.0.1:9000')
    DEBUG = True
    ALLOWED_HOSTS = []

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}