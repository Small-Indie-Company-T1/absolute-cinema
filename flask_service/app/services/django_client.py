import httpx
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class DjangoIntegrationError(Exception):
    """Базовая ошибка интеграции с Django"""
    ...

class DjangoTimeoutError(DjangoIntegrationError):
    """Timeout при подключении к django"""
    ...

class DjangoConnectionError(DjangoIntegrationError):
    """Ошибка подключения к Django"""
    ...

class MovieNotFoundError(Exception):
    """Фильм не найден в Django (404)"""
    ...

def check_movie_exists(movie_id: int) -> bool:
    """
    Проверяет, существует ли фильм в Django API.
    Возвращает True, если фильм есть.

    Raises:
        MovieNotFoundError: если фильм не найден (404)
        DjangoTimeoutError: при timeout подключения
        DjangoConnectionError: при ошибке подключения
        DjangoIntegrationError: при других ошибках Django API
    """
    django_url = current_app.config.get("DJANGO_API_URL")

    if not django_url:
        logger.error("DJANGO_API_URL not configured in app config")
        raise DjangoIntegrationError("Django API URL not configured")

    url = f"{django_url}/movies/{movie_id}/"

    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            logger.info(f"Movie {movie_id} exists")
            return True
        elif response.status_code == 404:
            logger.warning(f"Movie {movie_id} not found")
            raise MovieNotFoundError(f'Movie with id {movie_id} does not exist')
        else:
            logger.warning(f"Django returned {response.status_code}")
            raise DjangoIntegrationError(
                f'Django API returned {response.status_code}: {response.text}'
            )

    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to Django API for movie {movie_id}")
        raise DjangoTimeoutError(
            f'Timeout while checking movie {movie_id} in django'
        ) from e
    except httpx.ConnectError as e:
        logger.error(f"Cannot connect to Django API at {django_url}")
        raise DjangoConnectionError(
            f'Cannot connect to Django API at {django_url}'
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error checking movie {movie_id}: {e}")
        raise DjangoIntegrationError(
            f'Unexpected error checking movie with id {movie_id}'
        ) from e
