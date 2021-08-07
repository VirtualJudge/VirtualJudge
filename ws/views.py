from django.shortcuts import render
from channels.layers import get_channel_layer
# Create your views here.
from asgiref.sync import async_to_sync


def test():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("chat_ws", {"type": "ws.chat_message", 'message': "announcement_text"})
    # await channel_layer.group_send(
    #     'ws',
    #     {"type": "chat.system_message", "text": 'announcement_text'},
    # )
