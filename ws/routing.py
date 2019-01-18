from django.urls import path

from ws import consumers

websocket_urlpatterns = [
    path('api/ws_<str:chat_type>', consumers.ChatConsumer),
]
