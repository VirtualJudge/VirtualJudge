from django.urls import path
from account.views import LogoutAPI, LoginAPI, RegisterAPI, ProfileAPI, SessionAPI, ChangePasswordAPI, RankAPI, HookAPI

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("rank/", RankAPI.as_view(), name="rank"),
    path("hook/", HookAPI.as_view(), name="hook"),
    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('profile/change_password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('session/', SessionAPI.as_view(), name='session'),
]
