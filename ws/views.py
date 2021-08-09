# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def test():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("chat_ws", {"type": "chat.message", 'message': "announcement_text"})
