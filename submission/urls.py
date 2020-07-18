from django.urls import path
from submission import views

urlpatterns = [
    path('sample/', views.sample),
]
