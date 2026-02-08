from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Movie
from .serializers import MovieSerializer
from accounts.permissions import IsAdminRole
from genres.models import Genre


class MovieAdminViewSet(ModelViewSet):
    queryset = Movie.objects.all().order_by("-created_at")
    serializer_class = MovieSerializer
    permission_classes = [IsAdminRole]

    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["release_year", "created_at"]


def movies_page(request):
    genres = Genre.objects.all()
    return render(request, "movies.html", {"genres": genres})
