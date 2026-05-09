from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class UserApiTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('users-register')
        self.login_url = reverse('login')
        self.me_url = reverse('users-me')

    def test_register_success(self):
        data = {
            'email': 'user@example.com',
            'password': 'Hash456!',
            'password_confirm': 'Hash456!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_password_confirmation_fail(self):
        data = {
            'email': 'user@test.com',
            'password': 'Hash456',
            'password_confirm': 'Hash67',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(email='user@test.com', password='Hash456')
        response = self.client.post(
            self.login_url,
            {'email': 'user@test.com', 'password': 'Hash456'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_password_fail(self):
        User.objects.create_user(email='user@test.com', password='Hash456')
        response = self.client.post(
            self.login_url,
            {'email': 'user@test.com', 'password': 'Hash67'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me(self):
        user = User.objects.create_user(email='user@test.com', password='Hash456')
        self.client.force_authenticate(user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'user@test.com')
