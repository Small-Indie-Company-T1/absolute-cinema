from django.contrib import admin
from django.urls import path, include

from subscriptions.urls import router as subscription_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(subscription_router.urls)),
]
