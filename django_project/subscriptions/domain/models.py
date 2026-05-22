from datetime import timedelta

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from config.components.base_settings import AUTH_USER_MODEL


class SubscriptionManager(models.Manager):
    def active(self):
        return self.filter(end_date__gt=timezone.now())

    def for_user(self, user):
        return self.filter(user=user)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название плана")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дней)")

    class Meta:
        verbose_name = "План подписки"
        verbose_name_plural = "Планы подписок"
        ordering = ["price", "duration_days"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.PROTECT, related_name="user_subscriptions"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = SubscriptionManager()

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def clean(self):
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError("End date has to be later than start date")

    @property
    def is_active(self):
        if not self.end_date:
            return False
        return self.end_date > timezone.now()
