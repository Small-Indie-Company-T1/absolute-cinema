from django.db import models

from subscriptions.domain.models import SubscriptionPlan


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Жанры"
        verbose_name = "Жанр"

class MovieManager(models.Manager):
    def available_for(self, user):
        free_condition = models.Q(is_free=True)
        if user.is_authenticated:
            user_plans = user.subscriptions.active().values_list('plan_id', flat=True)
            return self.filter(free_condition | models.Q(available_in_plans__id__in=user_plans)).distinct()
        return self.filter(free_condition)

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    release_date = models.DateField(verbose_name="Дата выпуска")
    duration = models.PositiveIntegerField(verbose_name="Длительность (в минутах)")
    genre = models.ManyToManyField(Genre, related_name="movies", verbose_name="Жанр")
    available_in_plans = models.ManyToManyField(
        SubscriptionPlan,
        related_name="movies",
        verbose_name="Доступ в планах",
        blank=True
    )
    poster = models.ImageField(
        upload_to="movie_poster", blank=True, null=True, verbose_name="Постер"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_free = models.BooleanField(default=False)

    objects = MovieManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-release_date"]
