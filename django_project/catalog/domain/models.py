from django.db import models


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
    genre = models.ManyToManyField(Genre, related_name="movies", verbose_name="Жанр")
    poster = models.ImageField(
        upload_to="movie_poster", blank=True, null=True, verbose_name="Постер"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_free = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-release_date"]
