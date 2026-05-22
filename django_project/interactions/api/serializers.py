from rest_framework import serializers

from catalog.domain.models import Movie
from ..domain.models import Watchlist


class WatchlistSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Watchlist
        fields = ["movie", "added_at", "watched"]
        read_only_fields = ["added_at"]


class AddWatchlistSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Watchlist
        fields = ["movie"]


class RemoveWatchlistSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Watchlist
        fields = ["movie"]
