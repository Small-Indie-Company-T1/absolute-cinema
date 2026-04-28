from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    AddWatchlistSerializer,
    RemoveWatchlistSerializer,
    WatchlistSerializer,
)
from ..domain.models import Watchlist
from ..services.services import add_movie_to_watchlist, remove_movie_from_watchlist


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Watchlist.objects.filter(user=self.request.user)
        watched = self.request.query_params.get("watched")
        ordering = self.request.query_params.get("ordering")

        if watched is not None:
            if watched.lower() == "true":
                queryset = queryset.filter(watched=True)
            elif watched.lower() == "false":
                queryset = queryset.filter(watched=False)

        allowed_ordering = ["added_at", "-added_at", "watched", "-watched"]
        if ordering and ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-added_at")

        return queryset

    @action(detail=False, methods=["post"])
    def add_to_watchlist(self, request):
        serializer = AddWatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = serializer.validated_data["movie"]
        add_movie_to_watchlist(request.user, movie.id)

        return Response(
            {"status": "success", "message": "Фильм добавлен в список просмотра"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def remove_from_watchlist(self, request):
        serializer = RemoveWatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = serializer.validated_data["movie"]
        remove_movie_from_watchlist(request.user, movie.id)

        return Response(
            {"status": "success", "message": "Фильм удален из списка просмотра"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def mark_as_watched(self, request, pk=None):
        watchlist = self.get_object()
        watchlist.watched = True
        watchlist.save(update_fields=["watched"])

        return Response(
            {"status": "success", "message": "Фильм отмечен как просмотренный"},
            status=status.HTTP_200_OK,
        )
