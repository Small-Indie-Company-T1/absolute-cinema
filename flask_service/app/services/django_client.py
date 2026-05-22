import httpx
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def check_movie_exists(movie_id: int) -> bool:
    """
    Проверяет, существует ли фильм в Django API.
    Возвращает True, если фильм есть.
    """
    django_url = current_app.config.get("DJANGO_API_URL")

    if not django_url:
        logger.error("DJANGO_API_URL not configured in app config")
        return False

    url = f"{django_url}/movies/{movie_id}/"

    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            logger.info(f"Movie {movie_id} exists")
            return True
        elif response.status_code == 404:
            logger.warning(f"Movie {movie_id} not found")
            return False
        else:
            logger.warning(f"Django returned {response.status_code}")
            return False

    except httpx.TimeoutException:
        logger.error(f"Timeout connecting to Django API for movie {movie_id}")
        return False
    except httpx.ConnectError:
        logger.error(f"Cannot connect to Django API at {django_url}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking movie {movie_id}: {e}")
        return False
