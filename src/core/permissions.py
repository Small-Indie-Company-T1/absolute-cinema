from rest_framework import permissions


class HasActiveSubscription(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = bool(request.user and request.user.is_authenticated 
                    and request.user.subscriptions.filter(is_active=True).exists())
        return flag
    