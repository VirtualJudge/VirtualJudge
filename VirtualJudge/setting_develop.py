import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vj_database',
        'USER': 'vj_admin',
        'PASSWORD': 'vj_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

REDIS_CONF = {
    "host": "127.0.0.1",
    "port": "6379"
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
PUBLIC = '/public/'

