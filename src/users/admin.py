from django.contrib import admin
from subscriptions.models import Subscription

class SubscriptionInline(admin.TabularInline):
    """
    Инлайн чтобы подписки отображались прям в карточке юзера
    В будущий UserAdmin добавьте
    inlines = [SubscriptionInline]
    """
    model = Subscription
    extra = 0
