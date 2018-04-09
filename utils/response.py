from enum import Enum


class Message(Enum):
    DEFAULT = 0
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFO = 4


def success(information):
    return {
        'status': Message.SUCCESS.value,
        'message': information
    }


def warning(information):
    return {
        'status': Message.WARNING.value,
        'message': information
    }


def error(information):
    return {
        'status': Message.ERROR.value,
        'message': information
    }


def info(information):
    return {
        'status': Message.INFO.value,
        'message': information
    }


def default(information):
    return {
        'status': Message.DEFAULT.value,
        'message': information
    }
