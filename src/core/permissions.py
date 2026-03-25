from rest_framework import permissions

from django.utils import timezone


class HasActiveSubscription(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.subscriptions.filter(end_date__gt=timezone.now()).exists()
    