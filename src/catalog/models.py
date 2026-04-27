from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Жанры"
        verbose_name = "Жанр"

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    release_date = models.DateField(verbose_name="Дата выпуска")
    duration = models.PositiveIntegerField(verbose_name="Длительность (в минутах)")
    genre = models.ManyToManyField(Genre, related_name= "movies", verbose_name="Жанр")
    poster = models.ImageField(upload_to="movie_poster", blank=True, null=True, verbose_name="Постер")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['-release_date']

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="in_watchlist")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "movie"] # Нельзя добавить фильм дважды
        verbose_name = "Список просмотра"
        verbose_name_plural = "Списки просмотра"
    def __str__(self):
        return f"{self.user.email}-{self.movie.title}"



