from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_year', 'is_premium')
    list_filter = ('genre', 'is_premium')
    search_fields = ('title',)
