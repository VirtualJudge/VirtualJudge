from django.urls import path
from remote.views import RemoteAPI, RemoteLanguageAPI

urlpatterns = [
    path("remote", RemoteAPI.as_view(), name="remote"),
    path("languages/<str:remote_oj>", RemoteLanguageAPI.as_view(), name="remote_languages"),
]
