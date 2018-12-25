from django.urls import path

from statistic import views

urlpatterns = [
    path('statistic/submission', views.SubmissionAPI.as_view(), name='submission_statistic'),
]
