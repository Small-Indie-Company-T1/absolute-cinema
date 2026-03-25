from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from django.utils import timezone

from subscriptions.serializers import SubscriptionSerializer, SubscribeSerializer
from subscriptions.models import SubscriptionPlan, Subscription


class SubscribeViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data['plan_id']
        plan = SubscriptionPlan.objects.get(pk=plan_id)

        if Subscription.objects.active().filter(user=request.user, plan=plan).exists():
            return Response(
                {'warning': 'User already has an active subscription'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription = Subscription.objects.create(user=request.user, plan=plan)

        response_serializer = SubscriptionSerializer(subscription)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)




# class CurrentSubscriptionView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         sub = request.user.subscription.active().order_by('-start_date').first()

#         if sub:
#             serializer = SubscriptionSerializer(sub)
#             return Response(serializer.data)
        
#         return Response({'detail': 'No active subscriptions'}, status=404)
    
# class SubscribeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = SubscribeSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid:
#             sub = serializer.save()
#             response_serializer = SubscribeSerializer(sub)
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
