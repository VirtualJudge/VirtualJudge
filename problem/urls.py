from django.urls import path

from problem import views

urlpatterns = [
    path('get_problem_by_id', views.get_problem_by_id, name='get_problem_by_id'),
    path('get_problem_list', views.get_problem_list, name='get_problem_list'),
    path('get_problem_count', views.get_problem_count, name='get_problem_count'),
    path('get_problem_by_roj_and_rid', views.get_problem_by_roj_and_rid, name='get_problem_by_roj_and_rid'),
]
