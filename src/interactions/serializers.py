from rest_framework import serializers

from interactions.models import Watchlist


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["id", "movie", "added_at"]
        read_only_fields = ["added_at"]

    def validate(self, data): ...
