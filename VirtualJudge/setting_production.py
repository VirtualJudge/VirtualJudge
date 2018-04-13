from .utils import get_env

DEBUG = False

PUBLIC = '/public'
PUBLIC_DIR = '/public'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ), 'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ), 'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
