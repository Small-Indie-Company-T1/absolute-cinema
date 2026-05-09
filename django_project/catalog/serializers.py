from rest_framework import serializers
from .models import Genre, Movie


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
