from ..domain.models import Movie
from ..domain.exceptions import MovieNotFound


class MovieService:
    @staticmethod
    def get_all_movies():
        return Movie.objects.all().prefetch_related('genre')
    
    @staticmethod
    def get_movie_details(movie_id):
        try:
            return Movie.objects.prefetch_related('genre').get(pk=movie_id)
        except Movie.DoesNotExist:
            raise MovieNotFound("Movie not found")
