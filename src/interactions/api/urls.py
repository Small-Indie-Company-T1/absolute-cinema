from rest_framework.routers import DefaultRouter

from .views import WatchlistViewSet

router = DefaultRouter()
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
