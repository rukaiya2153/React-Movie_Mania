from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from movies.views import MovieAdminViewSet
from genres.views import GenreViewSet
from shows.views import ShowAdminViewSet, EpisodeAdminViewSet
from payments.views import PaymentAdminViewSet

# === ROUTER ===
router = DefaultRouter()
router.register(r"admin/movies", MovieAdminViewSet, basename="admin-movies")
router.register(r"admin/genres", GenreViewSet, basename="admin-genres")
router.register(r"admin/shows", ShowAdminViewSet, basename="admin-shows")
router.register(r"admin/episodes", EpisodeAdminViewSet, basename="admin-episodes")
router.register(r"admin/payments", PaymentAdminViewSet, basename="admin-payments")

# === URLPATTERNS ===
urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    path("api/", include(router.urls)),
    path("api/", include("accounts.urls")),
    path("api/", include("movies.urls")),
    path("api/", include("shows.urls")),

    # Pages
    path("", TemplateView.as_view(template_name="login.html")),
]

# === PAGE ROUTES (Import views locally to avoid circular import) ===
from accounts import views as accounts_views

urlpatterns += [
    path("dashboard/", accounts_views.dashboard_page),
    path("movies/", accounts_views.movies_page, name="movies"),
    path("tvshows/", accounts_views.tvshows_page),
    path("genres/", accounts_views.genres_page),
    path("users/", accounts_views.users_page),
    path("payments/", accounts_views.payments_page),
    path("reports/", accounts_views.reports_page),
]

# === MEDIA FILES (development only) ===
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
