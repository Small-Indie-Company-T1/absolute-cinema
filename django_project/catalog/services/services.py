from ..domain.models import Movie
from ..domain.exceptions import MovieNotFound
import requests
import logging
from django.conf import settings
from ..domain.exceptions import RecommendationServiceError
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)

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

    @staticmethod
    def get_user_recommendations(user):
        fastapi_url = getattr(settings, "FASTAPI_SERVICE_URL", "http://localhost:8001")
        endpoint = f"{fastapi_url}/api/v1/recommendations/me"

        logger.info(f"Fetching recommendations from FastAPI for user ID: {user.id}")

        token = str(AccessToken.for_user(user))

        params = {
            "token": token
        }

        try:
            response = requests.get(endpoint, params=params, timeout=5.0)

            if response.status_code != 200:
                logger.error(f"FastAPI returned error status: {response.status_code}")
                raise RecommendationServiceError(f"FastAPI returned status {response.status_code}")

            data = response.json()
            items = data.get("items", [])
            movie_ids = [item["movie"]["id"] for item in items if "movie" in item]

            if not movie_ids:
                return []

            movies = Movie.objects.prefetch_related('genre').filter(id__in=movie_ids)

            movie_dict = {m.id: m for m in movies}
            return [movie_dict[m_id] for m_id in movie_ids if m_id in movie_dict]

        except (requests.RequestException, ValueError) as e:
            logger.exception("Failed to connect or parse response from FastAPI recommendations service")
            raise RecommendationServiceError(f"Failed to fetch recommendations: {str(e)}")