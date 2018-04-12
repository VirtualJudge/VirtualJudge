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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ), 'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ), 'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
