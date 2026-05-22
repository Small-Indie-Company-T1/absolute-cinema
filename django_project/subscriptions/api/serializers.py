from datetime import timedelta

from rest_framework import serializers
from subscriptions.domain.models import Subscription, SubscriptionPlan
from django.utils import timezone


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "description", "price", "duration_days"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    is_active = serializers.SerializerMethodField()

    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ["id", "plan", "start_date", "end_date", "is_active", "time_left"]

    def get_is_active(self, obj):
        return obj.is_active

    def get_time_left(self, obj):
        if not obj.is_active:
            return None
        days = obj.end_date - timezone.now()
        return days if days > timedelta(days=0) else 0


class SubscribeSerializer(serializers.Serializer):
    """
    ОТдельный сериализатор для установки полей user и plan
    так как мы принимамем только plan_id
    """

    plan_id = serializers.IntegerField()

    def validate_plan_id(self, value):
        try:
            plan = SubscriptionPlan.objects.get(pk=value)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("No such plan")
        return value

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     plan = SubscriptionPlan.objects.get(pk=validated_data['plan_id'])
    #     subscription = Subscription.objects.create(user=user, plan=plan)
    #     return subscription
