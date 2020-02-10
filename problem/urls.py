from rest_framework import routers
from .views import ProblemViewSet

router = routers.SimpleRouter()
router.register(r'', ProblemViewSet, basename='problem')

urlpatterns = router.urls
