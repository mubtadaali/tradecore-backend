from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.constants import EMAIL_NOT_DELIVERABLE_ERR_MSG


class UserRegistrationTestCase(TestCase):
    def setUp(self) -> None:
        self.registration_url = '/api/users/'
        self.user = User.objects.create_user(username='rach', email='rach@friends.com', password='1234')
        self.not_deliverable_email_data = {
            "username": "rachelgreen", "first_name": "Rachel", "last_name": "Green",
            "email": "rachel@friends.com", "password": "test1234"
        }
        self.deliverable_email_success_data = {
            "username": "rachelgreen", "first_name": "Rachel", "last_name": "Green",
            "email": "mubtada.syed@gmail.com", "password": "test1234"
        }

    def test_not_deliverable_email_registration(self):
        client = APIClient()
        response = client.post(self.registration_url, self.not_deliverable_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(EMAIL_NOT_DELIVERABLE_ERR_MSG, response.json()['email'])

    def test_deliverable_email_success_registration(self):
        client = APIClient()
        response = client.post(self.registration_url, self.deliverable_email_success_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_email_already_exists(self):
        client = APIClient()
        data = self.not_deliverable_email_data
        data['email'] = self.user.email
        response = client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field must be unique.', response.json()['email'])

