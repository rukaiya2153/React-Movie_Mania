from rest_framework.viewsets import ModelViewSet
from .models import Genre
from .serializers import GenreSerializer
from rest_framework.permissions import IsAdminUser

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]
