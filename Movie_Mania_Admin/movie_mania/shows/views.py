from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Show, Episode
from .serializers import ShowSerializer, EpisodeSerializer

class ShowAdminViewSet(ModelViewSet):
    queryset = Show.objects.all().order_by("-created_at")
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]  # handle file uploads

class EpisodeAdminViewSet(ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdminUser]
