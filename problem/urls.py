from django.urls import path

from problem import views

urlpatterns = [
    path('problem/<int:problem_id>/', views.ProblemLocalAPI.as_view(),
         name='get_problem_from_local'),
    path('problem/<int:problem_id>/<str:param>/', views.ProblemLocalAPI.as_view(),
         name='get_problem_param_from_local'),
    path('problem/<str:remote_oj>/<str:remote_id>/', views.ProblemAPI.as_view(),
         name='get_problem_by_remote'),
    path('problem/refresh/<str:remote_oj>/<str:remote_id>/', views.ProblemRefreshAPI.as_view(),
         name='refresh_problem_by_remote'),
    path('problem/<str:remote_oj>/<str:remote_id>/html/', views.ProblemHtmlAPI.as_view(),
         name='get_problem_param_by_remote'),
    path('problems/', views.ProblemListAPI.as_view(), name='get_problem_list'),
]
