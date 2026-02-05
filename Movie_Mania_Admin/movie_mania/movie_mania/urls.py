"""
URL configuration for movie_mania project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for movie_mania project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ViewSets
from movies.views import MovieAdminViewSet
from genres.views import GenreViewSet
from shows.views import ShowAdminViewSet, EpisodeAdminViewSet
from payments.views import PaymentAdminViewSet
from reports.views import admin_dashboard


# Router
router = DefaultRouter()
router.register(r'admin/movies', MovieAdminViewSet, basename='admin-movies')
router.register(r'admin/genres', GenreViewSet, basename='admin-genres')
router.register(r'admin/shows', ShowAdminViewSet, basename='admin-shows')
router.register(r'admin/episodes', EpisodeAdminViewSet, basename='admin-episodes')
router.register(r'admin/payments', PaymentAdminViewSet, basename='admin-payments')


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Routes
    path('api/', include(router.urls)),

    # Admin Dashboard Stats
    path('api/admin/dashboard/', admin_dashboard, name='admin-dashboard'),
]
