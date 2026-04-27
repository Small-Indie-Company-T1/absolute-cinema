from django.contrib import admin
from .models import Genre, Movie, Watchlist

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "release_date", "duration"]
    list_filter = ["release_date", "genres"]
    search_fields = ["title", "description"]
    filter_horizontal = ["genres"]

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "movie", "added_at"]
    search_fields = ["added_at"]
    filter_horizontal = ["user_email", "movie_title"]