from websocket import create_connection

from VirtualJudge import settings
import json


class WebsocketClient:
    def __init__(self, chat_type, number):
        url = f'ws://127.0.0.1:8000/api/ws/{chat_type}/{number}/{settings.SECRET_KEY}'
        self._ws = create_connection(url)

    def send(self, message):
        self._ws.send(json.dumps({'message': message}))

    def close(self):
        self._ws.close()


class SimpleWsClient:
    def __init__(self, chat_type, message):
        url = f'ws://127.0.0.1:8000/api/ws/{chat_type}/{settings.SECRET_KEY}'
        self._ws = create_connection(url)
        self._ws.send(json.dumps({'message': message}))
        self._ws.close()


if __name__ == "__main__":
    SimpleWsClient('submission', 'testset')
