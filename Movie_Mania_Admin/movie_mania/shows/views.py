from rest_framework.viewsets import ModelViewSet
from .models import Show, Episode
from .serializers import ShowSerializer, EpisodeSerializer
from rest_framework.permissions import IsAdminUser

class ShowAdminViewSet(ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]

class EpisodeAdminViewSet(ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdminUser]
