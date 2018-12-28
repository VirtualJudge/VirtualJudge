from django.urls import path

from submission import views

urlpatterns = [
    path('submission', views.SubmissionAPI.as_view(), name='submission'),
    path('verdict/<int:submission_id>', views.VerdictAPI.as_view(), name='verdict'),
    path('reload/<int:submission_id>', views.Reload.as_view(), name='reload'),
]
