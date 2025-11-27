from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        # Data for a test user
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.me_url = reverse('profile')
        
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "applicant"
        }

    def test_registration(self):
        """Test that a user can register successfully"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")

    def test_login_and_access_protected_route(self):
        """Test full flow: Register -> Login -> Access Protected Route"""
        # 1. Register
        self.client.post(self.register_url, self.user_data)

        # 2. Login
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get Token
        access_token = response.data['access']
        self.assertTrue(access_token)

        # 3. Access Protected Route (Me)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response_me = self.client.get(self.me_url)
        
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)
        self.assertEqual(response_me.data['email'], self.user_data['email'])

    def test_access_denied_without_token(self):
        """Test that protected routes fail without a token"""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)