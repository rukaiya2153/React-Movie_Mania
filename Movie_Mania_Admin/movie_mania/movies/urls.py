from rest_framework.routers import DefaultRouter
from .views import MovieAdminViewSet

router = DefaultRouter()
router.register(r'admin/movies', MovieAdminViewSet, basename="admin-movies")

urlpatterns = router.urls
