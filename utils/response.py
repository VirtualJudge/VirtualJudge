from enum import Enum


class Message(Enum):
    SUCCESS = 0
    ERROR = 1


def res_format(raw_data, status=Message.SUCCESS):
    if status == Message.SUCCESS:
        return {
            'status': status.value,
            'data': raw_data
        }
    else:
        data = list()
        if isinstance(raw_data, dict):
            for k, v in raw_data.items():
                if isinstance(v, list):
                    data += v
                else:
                    data.append(v)
        elif isinstance(raw_data, str):
            data.append(raw_data)
        return {
            'status': status.value,
            'data': data
        }
