from rest_framework import status
from .models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):
    def setUp(self):
        self.login_url = '/v1/login/'
        self.access_url = '/v1/access/'

        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            is_active=True
        )

    def test_login_success(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, data)
        print(response.data, 'response')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)