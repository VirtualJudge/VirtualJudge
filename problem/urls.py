from django.urls import path

from problem import views

urlpatterns = [
    # path('get_problem_count', views.get_problem_count, name='get_problem_count'),
    path('problem/<int:problem_id>', views.get_problem_by_id, name='get_problem_by_id'),
    path('problem/<str:remote_oj>/<str:remote_id>', views.get_problem_by_roj_and_rid,
         name='get_problem_by_roj_and_rid'),

    path('problems', views.get_problem_list, name='get_problem_list'),
    path('problems/<int:offset>', views.get_problem_list, name='get_problem_list'),
    path('problems/<int:offset>/<int:limit>', views.get_problem_list, name='get_problem_list'),

]
