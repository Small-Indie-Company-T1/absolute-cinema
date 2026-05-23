from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..services.services import MovieService
from .serializers import MovieDetailSerializer, MovieSerializer, FastAPISearchResponseSerializer


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
        auth_header = request.headers.get('Authorization')
        recommended_movies = MovieService.get_user_recommendations(request.user, auth_header)

        serializer = self.get_serializer(recommended_movies, many=True)
        return Response(serializer.data)
    
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='recommendations/rebuild'
    )
    def rebuild_recommendations(self, request):
        auth_header = request.headers.get('Authorization')
        result = MovieService.rebuild_user_recommendations(request.user, auth_header)
        return Response(result, status=status.HTTP_202_ACCEPTED)

    @action(
        detail=False,
        methods=['get'],
        url_path='search'
    )
    def search(self, request):
        data = MovieService.search_movies(
            q=request.query_params.get("q"),
            genre_id=request.query_params.get("genre_id"),
            year_from=request.query_params.get("year_from"),
            year_to=request.query_params.get("year_to"),
            limit=request.query_params.get("limit", 10)
        )

        serializer = FastAPISearchResponseSerializer(
            instance=data
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )