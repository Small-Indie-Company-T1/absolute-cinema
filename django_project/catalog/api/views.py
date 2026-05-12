from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from ..services.services import MovieService
from .serializers import MovieDetailSerializer, MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MovieService.get_all_movies()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['genre', 'release_date']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    def get_queryset(self):
        return MovieService.get_all_movies()
