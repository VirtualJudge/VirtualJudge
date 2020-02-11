from rest_framework import routers
from django.urls import path
from user.views import UserAPI, PasswordAPI, AuthAPI, ProfileAPI, RegisterAPI

router = routers.SimpleRouter()
router.register('', UserAPI, basename='user')
urlpatterns = router.urls
urlpatterns += [
    path('auth/', AuthAPI.as_view()),
    path('myself/', ProfileAPI.as_view()),
    path('password/', PasswordAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
]
