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
import dj_database_url

ENVIRONMENT = os.getenv("ENVIRONMENT","localhost")
if ENVIRONMENT == "production":
    DEBUG = os.getenv("DEBUG",True)
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY",None)
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS",None)

    ALLOWED_HOSTS = ["*"]


    DB_INFO = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST' : os.getenv("DB_HOST"),
        'PORT' : os.getenv("DB_PORT"),
        'OPTIONS': {"sslmode": 'require'}
    }

    print(DEBUG)
    print(ALLOWED_HOSTS)
    print(SECRET_KEY)
    print(DB_INFO)
    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases
    DATABASES = {
        'default': DB_INFO
    }

else:
    from root.project_settings.development import *   

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'project.middleware.user_middleware.UserMiddleware',
]


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

ROOT_URLCONF = 'root.urls'
AUTH_USER_MODEL = 'project.User'
WSGI_APPLICATION = 'root.wsgi.application'

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

MEDIA_URL = '/uploadedfiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'project/uploadedfiles')


ERROR_LEVEL = 'WARNING' # DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
CORS_ORIGIN_ALLOW_ALL = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
} 

