from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from movies.views import MovieAdminViewSet
from genres.views import GenreViewSet
from shows.views import ShowAdminViewSet, EpisodeAdminViewSet
from payments.views import PaymentAdminViewSet

from accounts.views import (
    dashboard_page,
    movies_page,
    tvshows_page,
    genres_page,
    users_page,
    payments_page,
    reports_page,
)

router = DefaultRouter()
router.register(r"admin/movies", MovieAdminViewSet, basename="admin-movies")
router.register(r"admin/genres", GenreViewSet, basename="admin-genres")
router.register(r"admin/shows", ShowAdminViewSet, basename="admin-shows")
router.register(r"admin/episodes", EpisodeAdminViewSet, basename="admin-episodes")
router.register(r"admin/payments", PaymentAdminViewSet, basename="admin-payments")

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("api/", include(router.urls)),
    path("api/", include("accounts.urls")),

    # Pages
    path("", TemplateView.as_view(template_name="login.html")),
    path("dashboard/", dashboard_page),
    path("movies/", movies_page),
    path("tvshows/", tvshows_page),
    path("genres/", genres_page),
    path("users/", users_page),
    path("payments/", payments_page),
    path("reports/", reports_page),
]
