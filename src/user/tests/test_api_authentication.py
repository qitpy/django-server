'''
test user register, login, token authentication
'''

from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    User,
)

USER_GOOGLE_LOGIN_URL = reverse('user:login_with_google')
USER_LOGOUT_URL = reverse('user:knox_logoutall')
USER_LOGOUT = reverse('user:knox_logout')


def create_user(email='user@example.com',
                name='user example'):
    '''create and return a new user'''
    return get_user_model().objects.create_user(email, name)


class AuthenticationApiTests(TestCase):
    '''Test the public features of the user API'''

    def setUp(self):
        self.client = APIClient()

    @patch('user.utils.UserUtils.login_with_google_and_get_info')
    def test_user_login_via_google(self, google_auth_patched):
        """test that user login with google,
        then create new account if not existed
        return token to user"""
        user_email = 'user@example.com'
        user_name = 'Alex'
        user_google_credential = 'thisIsFakeCredentialThatClient\
            ReceiveAfterLoginSuccessWithGoogleAuthentication'
        google_auth_patched.return_value = (user_email, user_name)
        payload = {'credential': user_google_credential}
        res = self.client.post(USER_GOOGLE_LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print('*****', res.data)

        user = User.objects.get(pk=res.data['user']['id'])
        self.assertIsNotNone(user)
        self.assertEqual(user_email, user.email)
        self.assertEqual(user_name, user.name)
