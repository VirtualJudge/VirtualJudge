from django.urls import path

from submission import views

urlpatterns = [
    path('submission', views.SubmissionAPI.as_view(), name='submission'),
    path('verdict/<int:submission_id>', views.VerdictAPI.as_view(), name='verdict'),
    path('rejudge/<int:submission_id>', views.RejudgeAPI.as_view(), name='reload'),
]
