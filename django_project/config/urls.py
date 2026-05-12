from django.contrib import admin
from django.urls import path, include
from subscriptions.api.urls import router as subscription_router
from interactions.api.urls import router as interactions_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(subscription_router.urls)),
    path('api/users/', include('users.urls')),
    path('api/interactions/', include(interactions_router.urls)),
    path('api/', include('catalog.api.urls')),
]
