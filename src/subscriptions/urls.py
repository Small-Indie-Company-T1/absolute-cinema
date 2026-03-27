from rest_framework.routers import DefaultRouter

from subscriptions.views import SubscribeViewSet

router = DefaultRouter()
router.register(r'subscription', SubscribeViewSet, basename='subscription')