from rest_framework import routers

from .views import SubmissionViewSet

router = routers.SimpleRouter()
router.register(r'', SubmissionViewSet, basename='submission')
urlpatterns = router.urls
