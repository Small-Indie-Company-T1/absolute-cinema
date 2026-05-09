from subscriptions.models import Subscription, SubscriptionPlan


class SubscriptionAlreadyActive(Exception):
    ...

def subscribe_user_to_plan(user, plan_id):
    plan = SubscriptionPlan.objects.get(pk=plan_id)
    if Subscription.objects.active().filter(user=user, plan=plan).exists():
        raise SubscriptionAlreadyActive("Current plan is already active")
    return Subscription.objects.create(user=user, plan=plan)
