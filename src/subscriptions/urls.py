from rest_framework.routers import DefaultRouter

from subscriptions.views import SubscribeViewSet

router = DefaultRouter()
router.register(r'subscribe', SubscribeViewSet, basename='subscription')