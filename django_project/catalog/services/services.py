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
    def get_user_recommendations(user, auth_header: str | None = None):
        fastapi_url = getattr(settings, "FASTAPI_SERVICE_URL", "http://localhost:8001")
        endpoint = f"{fastapi_url}/api/v1/recommendations/me"

        logger.info(f"Fetching recommendations from FastAPI for user ID: {user.id}")

        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header
        else:
            token = str(AccessToken.for_user(user))
            headers['Authorization'] = f'Bearer {token}'

        try:
            response = requests.get(endpoint, headers=headers, timeout=5.0)

            if response.status_code == 401:
                logger.error("Unauthorized in recommendation service")
                raise RecommendationServiceError("Unauthorized in recommendation service")
            if response.status_code == 503:
                logger.error("Recommendation service unavailable")
                raise RecommendationServiceError("Recommendation service unavailable")
            if response.status_code == 502:
                logger.error("Recommendation service upstream error")
                raise RecommendationServiceError("Recommendation service upstream error")
            if response.status_code not in (200,):
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
        
    @staticmethod
    def rebuild_user_recommendations(user, auth_header: str | None = None):
        fastapi_url = getattr(settings, 'FASTAPI_SERVICE_URL', 'http://localhost:8001')
        endpoint = f'{fastapi_url}/api/v1/recommendations/rebuild'
        logger.info(f'Rebuilding recommendations for user: {user.id}')
        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header
        else:
            token = str(AccessToken.for_user(user))
            headers['Authorization'] = f'Bearer {token}'
        try:
            response = requests.post(endpoint, headers=headers, timeout=5.0)
            
            if response.status_code == 401:
                logger.error("Unauthorized in recommendation service")
                raise RecommendationServiceError("Unauthorized in recommendation service")
            if response.status_code == 503:
                logger.error("Recommendation service unavailable")
                raise RecommendationServiceError("Recommendation service unavailable")
            if response.status_code == 502:
                logger.error("Recommendation service upstream error")
                raise RecommendationServiceError("Recommendation service upstream error")
            if response.status_code not in (202,):
                logger.error(f"FastAPI returned error status: {response.status_code}")
                raise RecommendationServiceError(f"FastAPI returned status {response.status_code}")

            data = response.json()
            return data
        except (requests.RequestException, ValueError) as e:
            logger.exception("Failed to connect or parse response from FastAPI recommendations service")
            raise RecommendationServiceError(f"Failed to fetch recommendations: {str(e)}")
