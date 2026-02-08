from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Genre
from .serializers import GenreSerializer
from accounts.permissions import IsAdminRole


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminRole]


def genres_page(request):
    return render(request, "genres.html")
