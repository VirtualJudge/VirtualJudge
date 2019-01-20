from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class SimpleWsClient:
    def __init__(self, chat_type, message):
        self._chat_type = chat_type
        self._message = message
        self._channel_layer = get_channel_layer()

    def execute(self):
        async_to_sync(self._channel_layer.group_send)(f'chat_{self._chat_type}',
                                                      {
                                                          'type': 'chat_message',
                                                          'message': self._message
                                                      })
