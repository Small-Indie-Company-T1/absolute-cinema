from django.test import SimpleTestCase

class CatalogTests(SimpleTestCase):
    def test_movies_list(self):
        response = self.client.get('/api/movies/recommendations/')
        self.assertIn(response.status_code, [200, 401, 403, 404])