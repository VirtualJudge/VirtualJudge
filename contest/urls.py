from django.urls import path

from submission import views

urlpatterns = [
    path('contests', views.SubmissionAPI.as_view(), name='contest'),
    path('contest/<int:contest_id>/problems'),
    path('contest/<int:contest_id>/submissions'),
]
