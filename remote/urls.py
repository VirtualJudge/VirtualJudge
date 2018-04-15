from django.urls import path
from remote.views import RemoteAPI, LanguagesAPI, FreshLanguageAPI, SupportAPI

urlpatterns = [
    path("remote/", RemoteAPI.as_view(), name="remote"),
    path("languages/<str:raw_oj_name>/", LanguagesAPI.as_view(), name="languages"),
    path("language/", FreshLanguageAPI.as_view(), name="language"),
    path("support/", SupportAPI.as_view(), name="support"),

]
