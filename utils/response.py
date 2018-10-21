from enum import Enum


class Message(Enum):
    SUCCESS = 0
    ERROR = 1


def res_format(raw_data, status=Message.SUCCESS):
    return {
        'status': status.value,
        'data': raw_data
    }
