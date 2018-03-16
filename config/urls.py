from django.urls import path
from config.views import InitRemoteAPI

urlpatterns = [
    path("init_remote", InitRemoteAPI.as_view(), name="init_remote"),
]
