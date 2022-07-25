DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'ew*32x_+=b-g=4g%)111o2isb+)zn(^$6b#wtq_geuf9fy8@jocc%='

DB_NAME = "syntropy"
DB_USER = "postgres"
DB_PASSWORD = "123123"
DB_HOST = "localhost"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST' : DB_HOST,
        'PORT' : '',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aldesabido@gmail.com'
EMAIL_HOST_PASSWORD = 'qlkboyrkigtxunph'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER