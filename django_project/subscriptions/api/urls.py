from rest_framework.routers import DefaultRouter

from subscriptions.api.views import SubscribeViewSet

router = DefaultRouter()
router.register(r"subscription", SubscribeViewSet, basename="subscription")
