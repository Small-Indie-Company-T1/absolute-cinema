from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets

from subscriptions.serializers import SubscriptionSerializer, SubscribeSerializer
from subscriptions.models import SubscriptionPlan, Subscription


class SubscribeViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    @action(detail=False, methods=["post"], url_path="subscribe")
    def subscribe(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data["plan_id"]
        plan = SubscriptionPlan.objects.get(pk=plan_id)

        if Subscription.objects.active().filter(user=request.user, plan=plan).exists():
            return Response(
                {"warning": "Current plan is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = Subscription.objects.create(user=request.user, plan=plan)

        response_serializer = SubscriptionSerializer(subscription)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
