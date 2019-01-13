from django.urls import path

from ws import consumers

websocket_urlpatterns = [
    path('api/ws/<str:chat_type>/<str:number>', consumers.ChatConsumer),
    path('api/ws/<str:chat_type>/<str:number>/<str:secret_key>', consumers.ChatAdminConsumer),
]
