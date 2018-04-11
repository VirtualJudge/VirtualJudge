from django.urls import path
from config.views import InitRemoteAPI, RemoteLanguageAPI

urlpatterns = [
    path("init_remote", InitRemoteAPI.as_view(), name="init_remote"),
    path("languages/<str:remote_oj>", RemoteLanguageAPI.as_view(), name="remote_languages"),
]
