import os


def get_env(key, value=''):
    return os.environ.get(key, value)
