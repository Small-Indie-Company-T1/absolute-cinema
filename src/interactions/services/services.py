from django.db import IntegrityError
from ..models import Watchlist
from catalog.models import Movie


def add_movie_to_watchlist(user, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return None, "Фильм не найден."

    try:
        watchlist_entry, created = Watchlist.objects.get_or_create(
            user=user, movie=movie
        )

        if created:
            return watchlist_entry, None
        else:
            return None, "Фильм уже есть в списке"
    except IntegrityError:
        return None, "Ошибка при добавлении фильма в список"
