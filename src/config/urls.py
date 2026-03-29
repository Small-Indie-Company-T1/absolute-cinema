from django.contrib import admin
from django.urls import path, include
from users.urls import router as users_router
from subscriptions.urls import router as subscription_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(subscription_router.urls)),
    path('api/users/', include(users_router.urls)),

    path('api/users/', include('users.urls')),
]
