from django.urls import path

from surface import views

urlpatterns = [
    path('', views.problems),
    path('problem/', views.problem),
    path('submissions/', views.submissions),
    path('login/', views.login),
    path('register/', views.register),
]
