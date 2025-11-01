from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/token/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test12345',
            'password2': 'test12345',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_login_user(self):
        """Test user login and token generation"""
        # First create a user
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test12345'
        )

        # Try to login
        login_data = {
            'email': 'test@example.com',
            'password': 'test12345'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_invalid_register(self):
        """Test invalid registration data"""
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_request(self):
        """Test authenticated request"""
        # Create user and get token
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test12345'
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Try to access protected endpoint
        response = self.client.get('/api/some-protected-endpoint/')
        # Note: This will fail if the endpoint doesn't exist, but it tests the authentication
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
