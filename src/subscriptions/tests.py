from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from subscriptions.models import Subscription, SubscriptionPlan


User = get_user_model()

class SubscriptipnApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password='hash456'
        )
        self.plan = SubscriptionPlan.objects.create(
            name='Base',
            description='Base plan',
            price='199.99',
            duration_days=30
        )
        self.url = reverse('subscription-subscribe')

    def test_subscribe_success(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {'plan_id': self.plan.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, plan=self.plan).exists())

    def test_subscribe_duplicate(self):
        Subscription.objects.create(user=self.user, plan=self.plan)
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {'plan_id': self.plan.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_invalid_plan(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {'plan_id': 666}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
