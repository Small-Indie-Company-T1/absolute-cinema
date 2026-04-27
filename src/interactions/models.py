from django.db import models
from django.conf import settings


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey('catalog.Movie', on_delete=models.CASCADE, related_name='in_watchlist')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"