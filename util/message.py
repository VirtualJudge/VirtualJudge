from enum import Enum


class Message(Enum):
    ERROR = 1
    SUCCESS = 0

    @staticmethod
    def success(data=None, status=SUCCESS, msg='success'):
        return {
            'status': status,
            'data': data,
            'info': msg
        }

    @staticmethod
    def error(data=None, status=ERROR, msg='error'):
        return {
            'status': status,
            'data': data,
            'info': msg
        }
