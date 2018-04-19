from django.urls import path

from surface import views

urlpatterns = [
    path('', views.IndexAPI.as_view()),
    path('problem/', views.ProblemAPI.as_view()),
    path('problems/', views.ProblemsAPI.as_view()),

    path('submissions/', views.SubmisssionsAPI.as_view()),
    path('submission/', views.SubmisssionAPI.as_view()),

    path('contests/', views.ContestsAPI.as_view()),
    path('contest/new/', views.ContestNewAPI.as_view()),
    path('contest/', views.ContestsAPI.as_view()),

    path('login/', views.LoginAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
]
