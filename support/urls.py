from django.urls import path

from support.views import AccountAPI, LanguageAPI, SupportAPI, SupportAdminAPI

urlpatterns = [
    path("language", LanguageAPI.as_view(), name="language"),
    path("support", SupportAPI.as_view(), name="support"),
    path("admin/support", SupportAdminAPI.as_view(), name="admin_support"),
    path("admin/spider", AccountAPI.as_view(), name="admin_spider")
]
