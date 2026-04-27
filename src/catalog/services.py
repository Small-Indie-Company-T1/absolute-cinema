from django.db import IntegrityError
from .models import Watchlist, Movie


def add_movie_to_watchlist(movie_id, user): #для добавления фильма в список просмотра
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return None, "Фильм не найден."

    try:
        watсhlist_entry, created = Watchlist.objects.get_or_create(user=user, movie=movie)

        if created:
            return watсhlist_entry, None
        else:
            return None, "Фильм уже есть в списке"
    except IntegrityError:
        return None, "Ошибка при добавлении фильма в список"
