from django.contrib import admin
from subscriptions.models import SubscriptionPlan

@admin.register(SubscriptionPlan)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name', 'description')