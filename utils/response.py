import json
from enum import Enum


class Message(Enum):
    DEFAULT = 0
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFO = 4


def success(data):
    return json.dumps({
        'status': Message.SUCCESS.value,
        'data': data
    }, indent=4)


def warning(data):
    return json.dumps({
        'status': Message.WARNING.value,
        'data': data
    }, indent=4)


def error(data):
    return json.dumps({
        'status': Message.ERROR.value,
        'data': data
    }, indent=4)


def info(data):
    return json.dumps({
        'status': Message.INFO.value,
        'data': data
    }, indent=4)


def default(data):
    return json.dumps({
        'status': Message.DEFAULT.value,
        'message': data
    }, indent=4)
