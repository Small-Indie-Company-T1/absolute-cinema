class MovieNotFound(Exception):
    """Исключение, возникающее при попытке добавить фильм, которого не существует."""

    pass


class MovieAlreadyInWatchlist(Exception):
    """Исключение, возникающее при попытке добавить фильм, который уже есть в списке избранного."""

    pass
