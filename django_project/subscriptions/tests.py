from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from subscriptions.domain.models import Subscription, SubscriptionPlan
from subscriptions.services.services import subscribe_user_to_plan
from subscriptions.domain.exceptions import SubscriptionAlreadyActive


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

class SubscriptionServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='hash456'
        )
        self.plan = SubscriptionPlan.objects.create(
            name='Base',
            description='Base plan',
            price='199.99',
            duration_days=30
        )

    def test_subscribe_to_plan_success(self):
        subscription = subscribe_user_to_plan(self.user, self.plan.id)
        self.assertIsNotNone(subscription)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, plan=self.plan).exists()
        )

    def test_subscribe_to_plan_already_active(self):
        Subscription.objects.create(user=self.user, plan=self.plan)
        with self.assertRaises(SubscriptionAlreadyActive):
            subscribe_user_to_plan(self.user, self.plan.id)
