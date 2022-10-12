'''
Test for the create token API
'''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')

def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)

class TokenApiTests(TestCase):
    '''Test the public features of the user API'''

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        '''test generates token for valid credential'''
        user_details = {
            'name': 'Test name',
            'email': 'test@example.com',
            'password': 'password',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        '''test return error if credentials invalid'''
        create_user(email='test@example.com', password='goodPass')

        payload = {
            'email': 'test@example.com',
            'password': 'BadPass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        '''test posting a blank password returns an error'''
        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
