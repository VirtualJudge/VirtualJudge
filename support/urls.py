from django.urls import path

from support.views import AccountAPI, LanguagesAPI, FreshLanguageAPI, SupportAPI

urlpatterns = [
    path("languages/<str:raw_oj_name>/", LanguagesAPI.as_view(), name="languages"),
    path("language/", FreshLanguageAPI.as_view(), name="language"),
    path("support/", SupportAPI.as_view(), name="support"),
    path("account/", AccountAPI.as_view(), name="account"),
]
