import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.posts.models import Post


class CommentCreationTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='rach', email='rach@friends.com', password='test1234')
        post_data = {
            "text": "Contrary to popular belief, Lorem Ipsum is not simply random text. "
                    "It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old",
            "author": self.user
        }
        self.post = Post.objects.create(**post_data)
        self.url = f'/api/posts/{self.post.id}/comments/'

        self.login_client = APIClient()
        response = self.login_client.post(
            reverse('token_obtain_pair'), json.dumps({'username': 'rach', 'password': 'test1234'}),
            content_type='application/json'
        )
        self.login_client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])

    def test_comment_creation_success(self):
        response = self.login_client.post(self.url, {'text': 'Contrary to popular belief, Lorem '}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_text_required_failure(self):
        response = self.login_client.post(self.url, {'text': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json()['text'])

    def test_not_authorized_failure(self):
        client = APIClient()
        response = client.post(self.url, {'text': 'Contrary to popular belief, Lorem '}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
