from django.contrib import admin

from .domain.models import Watchlist

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('added_at',)