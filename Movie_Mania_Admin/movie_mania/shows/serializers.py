from rest_framework import serializers
from .models import Show, Episode

class ShowSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False)  # optional for update

    class Meta:
        model = Show
        fields = "__all__"

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"
