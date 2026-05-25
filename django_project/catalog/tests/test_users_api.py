from django.test import SimpleTestCase

class UserTests(SimpleTestCase):
    def test_users_endpoint(self):
        response = self.client.get('/api/users/login/')
        self.assertIn(response.status_code, [200, 405])