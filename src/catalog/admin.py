from django.contrib import admin
from .models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "release_date", "duration"]
    list_filter = ["release_date", "genre"]
    search_fields = ["title", "description"]
    filter_horizontal = ["genre"]
