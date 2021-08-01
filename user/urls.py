from rest_framework.routers import SimpleRouter

from user.views import UserViewSet, AdvancedUserViewSet

router = SimpleRouter()
router.register('advanced', AdvancedUserViewSet, basename='advanced-user')
router.register('', UserViewSet, basename='user')
urlpatterns = router.urls
