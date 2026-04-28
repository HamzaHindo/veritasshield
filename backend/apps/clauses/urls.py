from rest_framework.routers import DefaultRouter

from .views import ClauseViewSet

router = DefaultRouter()
router.register(r"clauses", ClauseViewSet, basename="clause")

urlpatterns = router.urls
