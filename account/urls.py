from django.urls import path
from account import views

urlpatterns = [
    path('register', views.RegisterAPI.as_view(), name='register'),
    path('login', views.LoginAPI.as_view(), name='login'),
    path('logout', views.LogoutAPI.as_view(), name='logout')
]
