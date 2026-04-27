from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from subscriptions.models import Subscription

class SubscriptionInline(admin.TabularInline):
    """
    Инлайн чтобы подписки отображались прям в карточке юзера
    В будущий UserAdmin добавьте
    inlines = [SubscriptionInline]
    """
    model = Subscription
    extra = 0

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_premium', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('is_premium_status',)

    inlines = [SubscriptionInline]

    def is_premium_status(self, obj):
        return obj.is_premium

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name'),
        }),
    )