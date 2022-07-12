DEBUG = False
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ['SECRET_KEY']

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']