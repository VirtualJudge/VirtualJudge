from django.urls import path

from problem import views

urlpatterns = [
    # path('get_problem_count', views.get_problem_count, name='get_problem_count'),
    path('problem/<int:problem_id>', views.ProblemLocalAPI.as_view(), name='get_problem_from_local'),
    path('problem/<str:remote_oj>/<str:remote_id>', views.ProblemRemoteAPI.as_view(),
         name='get_problem_from_remote'),
    path('problem/<str:remote_oj>/<str:remote_id>/fresh', views.ProblemRemoteAPI.as_view(force_update=True),
         name='get_problem_from_remote'),

    path('problems', views.ProblemListAPI.as_view(), name='get_problem_list'),
    path('problems/<int:offset>', views.ProblemListAPI.as_view(), name='get_problem_list'),
    path('problems/<int:offset>/<int:limit>', views.ProblemListAPI.as_view(), name='get_problem_list'),

]
