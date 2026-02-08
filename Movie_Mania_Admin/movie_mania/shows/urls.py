from rest_framework.routers import DefaultRouter
from .views import ShowAdminViewSet, EpisodeAdminViewSet

router = DefaultRouter()
router.register(r'admin/shows', ShowAdminViewSet, basename='admin-shows')
router.register(r'admin/episodes', EpisodeAdminViewSet, basename='admin-episodes')

urlpatterns = router.urls
