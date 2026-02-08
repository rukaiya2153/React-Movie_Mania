from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source="genre.name", read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

def get_thumbnail(self, obj):
    request = self.context.get("request")
    if obj.thumbnail and request:
        return request.build_absolute_uri(obj.thumbnail.url)
        return None