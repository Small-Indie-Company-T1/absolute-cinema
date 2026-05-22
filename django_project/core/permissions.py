from rest_framework import permissions

from django.utils import timezone


class HasActiveSubscription(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:  # type: ignore
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.subscriptions.active().exists()
