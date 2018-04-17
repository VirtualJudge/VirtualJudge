from django.urls import path

from surface import views

urlpatterns = [
    path('', views.index),
    path('problem/', views.problem),
    path('problems/', views.problems),

    path('submissions/', views.submissions),
    path('submission/', views.submissions),

    path('contests/', views.contests),
    path('contest/new/', views.contest_new),
    path('contest/', views.contests),

    path('login/', views.login),
    path('register/', views.register),
]
