from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

# Routers for other apps
from movies.views import MovieAdminViewSet
from genres.views import GenreViewSet
from shows.views import ShowAdminViewSet, EpisodeAdminViewSet
from payments.views import PaymentAdminViewSet

router = DefaultRouter()
router.register(r'admin/movies', MovieAdminViewSet, basename='admin-movies')
router.register(r'admin/genres', GenreViewSet, basename='admin-genres')
router.register(r'admin/shows', ShowAdminViewSet, basename='admin-shows')
router.register(r'admin/episodes', EpisodeAdminViewSet, basename='admin-episodes')
router.register(r'admin/payments', PaymentAdminViewSet, basename='admin-payments')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include API routes
    path('api/', include(router.urls)),
    path('api/', include('accounts.urls')),  # login, OTP, dashboard-data

    # Login page as default
    path("", TemplateView.as_view(template_name="login.html")),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),

]
