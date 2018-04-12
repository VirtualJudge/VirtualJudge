import json
from enum import Enum


class Message(Enum):
    SUCCESS = 0
    ERROR = 1


def res_format(data, status=Message.SUCCESS):
    return {
        'status': status.value,
        'data': data
    }
