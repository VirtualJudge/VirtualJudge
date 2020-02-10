from rest_framework import routers
from problem.admin_views import AdminProblemViewSet

router = routers.SimpleRouter()

router.register('problem', AdminProblemViewSet, 'problem')

urlpatterns = router.get_urls()
