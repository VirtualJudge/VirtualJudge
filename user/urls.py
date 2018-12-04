from django.urls import path
from user.views import AuthAPI, RegisterAPI, ProfileAPI, ChangePasswordAPI, RankAPI, HookAPI,PrivilegeAPI

urlpatterns = [
    path("auth/", AuthAPI.as_view(), name="auth"),
    path("privilege/", PrivilegeAPI.as_view(), name="privilege"),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("rank/", RankAPI.as_view(), name="rank"),
    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('profile/change_password/', ChangePasswordAPI.as_view(), name='change_password'),
    path("profile/hook/", HookAPI.as_view(), name="hook"),
]
