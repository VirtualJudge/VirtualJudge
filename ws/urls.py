from django.urls import path, re_path

from ws import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>', consumers.ChatConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     path('ws/<str:chat_type>', consumers.ChatConsumer),
# ]
