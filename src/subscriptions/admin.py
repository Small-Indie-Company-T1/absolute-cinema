from django.contrib import admin
from subscriptions.models import SubscriptionPlan, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_days')
    search_fields = ('name', 'description',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active_status')
    list_filter = ('plan', 'start_date')

    @admin.display(boolean=True, description='Активна')
    def is_active_status(self, obj):
        return obj.is_active