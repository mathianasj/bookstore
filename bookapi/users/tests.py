from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your tests here.
class UserTest(APITestCase):
    def test_list_users(self):
        """
        Ensure we can get the list of users
        """
        user = User()
        user.set_password("abcdef")
        user.save()

        url = '/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_password_masked(self):
        """
        Ensure the password is mask on the user's list
        """
        user = User()
        user.set_password("abcdef")
        user.save()

        url = '/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse('password' in response.data[0])