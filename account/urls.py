from django.urls import path
from account.views import AuthAPI, RegisterAPI, ProfileAPI, ChangePasswordAPI, RankAPI, HookAPI

urlpatterns = [
    path("auth/", AuthAPI.as_view(), name="auth"),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("rank/", RankAPI.as_view(), name="rank"),
    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('profile/change_password/', ChangePasswordAPI.as_view(), name='change_password'),
    path("profile/hook/", HookAPI.as_view(), name="hook"),
]
