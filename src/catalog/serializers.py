from rest_framework import serializers
from .models import Genre, Movie, Watchlist

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "release_date", "description", "genres", "poster"]

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = "__all__"

class AddToWatchlistSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, value):
        if not Movie.objects.filter(id=value).exists():
            raise serializers.ValidationError("Фильма с таким айди нет")
        return value