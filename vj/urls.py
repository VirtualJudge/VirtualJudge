"""vj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from utils import views as utils_views
from vj.settings import DEBUG

urlpatterns = [
    path('api/admin/', admin.site.urls),
] if DEBUG else []

urlpatterns += [
    path('api/captcha/', utils_views.CaptchaAPI.as_view()),
    path('api/platform/', utils_views.PlatformAPI.as_view()),
    path('api/language/<str:remote_oj>/', utils_views.LanguageAPI.as_view()),
    path('api/user/', include('user.urls')),
    path('api/problem/', include('problem.urls')),
    path('api/submission/', include('submission.urls')),
]
