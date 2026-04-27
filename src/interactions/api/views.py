from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import WatchlistSerializer
from ..domain.models import Watchlist
from ..services.services import add_movie_to_watchlist


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_to_watchlist(self, request):
        serializer = WatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = serializer.validated_data['movie']

        add_movie_to_watchlist(request.user, movie.id)

        return Response({"status":"success", "message": "Фильм добавлен в список просмотра"}, status=status.HTTP_201_CREATED)
