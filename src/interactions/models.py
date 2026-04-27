from django.db import models

# Create your models here.
class Watchlist(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return self.user.username