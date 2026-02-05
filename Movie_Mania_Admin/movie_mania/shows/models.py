from django.db import models
from genres.models import Genre

class Show(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    total_seasons = models.IntegerField()
    thumbnail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    video_url = models.CharField(max_length=255)
    duration = models.IntegerField()
