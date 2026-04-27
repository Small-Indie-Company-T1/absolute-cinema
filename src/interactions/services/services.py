from django.db import IntegrityError
from catalog.models import Movie
from ..domain.models import Watchlist
from ..domain.exceptions import MovieNotFound, MovieAlreadyInWatchlist

def add_movie_to_watchlist(user, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise MovieNotFound("Фильм не найден")

    watchlist_entry, created = Watchlist.objects.get_or_create(user=user, movie=movie)

    if created:
        return watchlist_entry
    else:
        raise MovieAlreadyInWatchlist("Фильм уже в списке просмотра")
