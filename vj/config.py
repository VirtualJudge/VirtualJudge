import os

# Redis Config

REDIS_USER = os.getenv('REDIS_USER', None)
REDIS_PASS = os.getenv('REDIS_PASS', None)
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

# RabbitMQ Config

MQ_USER = os.getenv('MQ_USER', 'vj_user')
MQ_PASS = os.getenv('MQ_PASS', 'vj_pass')
MQ_HOST = os.getenv('MQ_HOST', '127.0.0.1')
MQ_PORT = os.getenv('MQ_PORT', 5672)

# Celery

BROKER_URL = f'amqp://{MQ_USER}:{MQ_PASS}@{MQ_HOST}:{MQ_PORT}/'

# Env

VJ_ENV = os.getenv('VJ_ENV', 'develop')

# PostgreSQL

PG_HOST = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DB = os.getenv('PG_DB', 'vj_db')
PG_USER = os.getenv('PG_USER', 'vj_user')
PG_PASS = os.getenv('PG_PASS', 'vj_pass')

# SMTP

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT', 465)
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')
SMTP_USE_SSL = (SMTP_PORT == 465)
DEFAULT_FROM_EMAIL = SMTP_USER
