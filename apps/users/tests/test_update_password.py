import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.constants import INVALID_EXISTING_PASSWORD_ERR_MSG


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='rach', email='rach@friends.com', password='1234')
        self.url = f'/api/users/{self.user.id}/update_password/'

    def test_update_password_not_authorized_failure(self):
        client = APIClient()
        response = client.patch(
            self.url, json.dumps({'old_password': '1234', 'new_password': 'abcd'}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_password_failure(self):
        client = APIClient()
        response = client.post(reverse('token_obtain_pair'), json.dumps({'username': 'rach', 'password': '1234'}),
                               content_type='application/json')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])
        response = client.patch(
            self.url, json.dumps({'old_password': 'abcd', 'new_password': 'test1234abc'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(INVALID_EXISTING_PASSWORD_ERR_MSG, response.json()['old_password'])

    def test_update_password_success(self):
        client = APIClient()
        response = client.post(reverse('token_obtain_pair'), json.dumps({'username': 'rach', 'password': '1234'}),
                               content_type='application/json')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])
        response = client.patch(
            self.url, json.dumps({'old_password': '1234', 'new_password': 'test1234abc'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
