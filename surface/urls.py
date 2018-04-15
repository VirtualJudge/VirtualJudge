from django.urls import path

from surface import views

urlpatterns = [
    path('', views.index),
    path('problem/', views.problem),
    path('status/', views.status),
    path('login/', views.login),
    path('register/', views.register),
]
