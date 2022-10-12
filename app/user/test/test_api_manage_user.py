'''
Test for the manage user API
'''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

ME_URL = reverse('user:me')

def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)

class PublicManageUserTests(TestCase):
    '''Test the public features of the user API'''
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_user_unauthorized(self):
            '''Test authentication is required for users'''
            res = self.client.get(ME_URL)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateManageUserTests(TestCase):
    '''Test API request that require authentication'''

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''test retrieving profile for logged in user'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        '''test POST is not allowed for the me endpoint'''
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''test updating the user profile for the authenticated user'''
        payload = {'name': 'Updated name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
