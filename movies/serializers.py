from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'genre',
            'genre_name',
            'release_year',
            'thumbnail',
            'trailer_url',
            'is_premium',
            'created_at',
        ]
