from django.urls import path

from problem import views

urlpatterns = [
    path('problem/<str:remote_oj>/<str:remote_id>', views.ProblemAPI.as_view(),
         name='get_problem'),
    path('problem', views.ProblemListAPI.as_view(), name='get_problem_list'),
]
