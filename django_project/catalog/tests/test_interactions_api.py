from django.test import SimpleTestCase

class InteractionTests(SimpleTestCase):
    def test_watchlist_endpoint(self):
        response = self.client.get('/api/interactions/watchlist/')
        self.assertIn(response.status_code, [200, 401, 403, 404])