import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.posts.models import Post


class PostCreationTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='rachel', email='rach@friends.com', password='test1234')
        post_data = {
            "text": "to popular belief, Lorem Ipsum is not simply random text. "
                    "It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old",
            "author": self.user
        }
        post = Post.objects.create(**post_data)
        self.like_url = f'/api/posts/{post.id}/like/'

        dislike_post = Post.objects.create(author=self.user, text='same random text here')
        self.dislike_url = f'/api/posts/{dislike_post.id}/dislike/'

        self.login_client = APIClient()
        response = self.login_client.post(
            reverse('token_obtain_pair'), json.dumps({'username': 'rachel', 'password': 'test1234'}),
            content_type='application/json'
        )
        self.login_client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])

    def test_post_like_success(self):
        response = self.login_client.get(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_like_count_success(self):
        post = Post.objects.create(author=self.user, text='same random text here')
        self.like_url = f'/api/posts/{post.id}/like/'
        response = self.login_client.get(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.login_client.get(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['likes'], 1)

    def test_post_like_dislike_count_success(self):
        post = Post.objects.create(author=self.user, text='same random text here')
        self.login_client.get(f'/api/posts/{post.id}/like/')
        self.login_client.get(f'/api/posts/{post.id}/dislike/')
        response = self.login_client.get(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 1)

    def test_post_dislike_success(self):
        response = self.login_client.get(self.dislike_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authorized_failure(self):
        client = APIClient()
        response = client.get(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
