from django.contrib import admin
from .domain.models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_free", "release_date", "duration"]
    list_filter = ["is_free", "available_in_plans", "release_date", "genre"]
    search_fields = ["title", "description"]
    filter_horizontal = ["genre", "available_in_plans"]

    fieldsets = (
        (
            None, {
                'fields': ('title', 'description', 'release_date', 'duration', 'genre')
            }
        ),
        (
            'Доступность', {
                'fields': ('is_free', 'available_in_plans'),
                'description': ('Если флаг is_free не установлен, выберите планы подписок')
            }
        ),
    )
