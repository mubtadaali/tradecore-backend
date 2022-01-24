import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='rach', email='rach@friends.com', password='1234')

    def test_login_success(self):
        client = APIClient()
        response = client.post(
            reverse('token_obtain_pair'),
            json.dumps({'username': 'rach', 'password': '1234'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json().keys())

    def test_login_failure(self):
        client = APIClient()
        response = client.post(
            reverse('token_obtain_pair'),
            json.dumps({'username': 'rach', 'password': 'abcd'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
