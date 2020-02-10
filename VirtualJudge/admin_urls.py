from rest_framework import routers
from problem.admin_views import AdminProblemViewSet
from destination.admin_views import AdminLanguageViewSet, AdminPlatformViewSet

router = routers.SimpleRouter()

router.register('problem', AdminProblemViewSet, 'problem')
router.register('platform', AdminPlatformViewSet, 'platform')
router.register('language', AdminLanguageViewSet, 'language')

urlpatterns = router.get_urls()
