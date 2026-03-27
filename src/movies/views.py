from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer, AddToWatchlistSerializer
from .services import add_movie_to_watchlist

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().prefetch_related('genres')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['genres', 'release_date']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_watchlist(self, request):
        serializer = AddToWatchlistSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        movie_id = serializer.validated_data['movie_id']
        watchlist_entry, error = add_movie_to_watchlist(request.user, movie_id)
        if error:
            return Response({"status":"error", "message": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":"success", "message": "Фильм добавлен в список просмотра"}, status=status.HTTP_201_CREATED)














