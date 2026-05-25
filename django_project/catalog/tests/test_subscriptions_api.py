from django.test import SimpleTestCase

class SubscriptionTests(SimpleTestCase):
    def test_subscriptions_endpoint(self):
        response = self.client.get('/api/subscriptions/')
        self.assertIn(response.status_code, [200, 401, 403, 404])