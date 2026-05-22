from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='recommendations'
    )
    def recommendations(self, request):
        """
        GET /api/v1/catalog/movies/recommendations/
        """
        recommended_movies = MovieService.get_user_recommendations(request.user)

        serializer = self.get_serializer(recommended_movies, many=True)
        return Response(serializer.data)