from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets

from subscriptions.api.serializers import SubscriptionSerializer, SubscribeSerializer
from subscriptions.services.services import subscribe_user_to_plan


class SubscribeViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    @action(detail=False, methods=["post"], url_path="subscribe")
    def subscribe(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = subscribe_user_to_plan(
            request.user, serializer.validated_data.get('plan_id')
        )

        return Response(
            SubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )
