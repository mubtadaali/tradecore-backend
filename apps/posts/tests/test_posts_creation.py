import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PostCreationTestCase(TestCase):
    def setUp(self) -> None:
        self.url = '/api/posts/'
        self.user = User.objects.create_user(username='rach', email='rach@friends.com', password='test1234')
        self.success_data = {
            "text": "Contrary to popular belief, Lorem Ipsum is not simply random text. "
                    "It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old"
        }

        self.login_client = APIClient()
        response = self.login_client.post(
            reverse('token_obtain_pair'), json.dumps({'username': 'rach', 'password': 'test1234'}),
            content_type='application/json'
        )
        self.login_client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])

    def test_post_creation_success(self):
        response = self.login_client.post(self.url, self.success_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_text_required_failure(self):
        response = self.login_client.post(self.url, {'text': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json()['text'])

    def test_not_authorized_failure(self):
        client = APIClient()
        response = client.post(self.url, self.success_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
