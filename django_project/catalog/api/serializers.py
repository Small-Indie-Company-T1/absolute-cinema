from rest_framework import serializers
from ..domain.models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(source='genre', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "release_date", "description", "genres", "poster"]


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(source='genre', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'release_date',
            'duration',
            'poster',
            'genres',
            'created_at',
            'updated_at'
        ]


class FastAPIGenreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class FastAPISearchMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    release_date = serializers.DateField()

    duration = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    poster = serializers.CharField(
        required=False,
        allow_null=True
    )

    genres = FastAPIGenreSerializer(many=True)


class FastAPISearchResponseSerializer(serializers.Serializer):
    items = FastAPISearchMovieSerializer(many=True)
    total = serializers.IntegerField()