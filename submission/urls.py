from django.urls import path

from submission import views

urlpatterns = [

    path('submission', views.SubmissionAPI.as_view(), name='submission'),
    path('verdict/<int:submission_id>', views.VerdictAPI.as_view(), name='verdict'),
    path('submission/<int:submission_id>', views.SubmissionShowAPI.as_view(), name='submission_show'),
    path('submissions', views.SubmissionListAPI.as_view(), name='submissions'),
    path('submissions/<int:offset>', views.SubmissionListAPI.as_view(), name='submissions'),
    path('rejudge/<int:submission_id>', views.ReJudgeAPI.as_view(), name='rejudge'),
]
