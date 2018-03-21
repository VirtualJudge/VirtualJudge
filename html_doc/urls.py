from django.urls import path
from html_doc import views

urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home_page'),
    path('login', views.LoginAPI.as_view(), name='login_page'),
    path('register', views.RegisterAPI.as_view(), name='register_page'),
]
