DEBUG = False
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.getenv("SECRET_KEY",None)

DB_NAME = os.getenv("DB_NAME",None)
DB_USER = os.getenv("DB_USER",None)
DB_PASSWORD = os.getenv("DB_PASSWORD",None)
DB_HOST = os.getenv("DB_HOST",None)