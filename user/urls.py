from rest_framework import routers

from user.views import UserViewSet, PasswordViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'user/password', PasswordViewSet, basename='password')

urlpatterns = router.urls
