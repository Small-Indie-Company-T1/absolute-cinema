from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from interactions.domain.exceptions import MovieNotFound, MovieAlreadyInWatchlist
from subscriptions.domain.exceptions import SubscriptionAlreadyActive
from catalog.domain.exceptions import MovieNotFound as CatalogMovieNotFound


def custom_exception_handler(exc, ctx):
    response = exception_handler(exc, ctx)

    if isinstance(exc, CatalogMovieNotFound):
        return Response(
            {'status': 'error', 'code': 404, 'message': 'Фильм не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, MovieNotFound):
        return Response(
            {'status': 'error', 'code': 404, 'message': 'Фильм не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, MovieAlreadyInWatchlist):
        return Response(
            {'status': 'error', 'code': 400, 'message': 'Фильм уже в списке просмотра'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, SubscriptionAlreadyActive):
        return Response(
            {'status': 'error', 'code': 400, 'message': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

    if response is not None:
        data = {
            'status': 'error',
            'code': response.status_code,
            'message': response.data
        }
        response.data = data

    return response
