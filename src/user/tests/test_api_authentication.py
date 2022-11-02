# '''
# test user register, login, token authentication
# '''
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# from core.models import (
#     User,
# )


# USER_REGISTER_URL = reverse('user:register')
# USER_LOGIN_URL = reverse('user:login')


# def create_user(**params):
#     '''create and return a new user'''
#     return get_user_model().objects.create_user(**params)


# phone_number_example = '+84123456789'
# email_example = 'email@example.com'
# name_example ='username example'
# password_example = 'PasswordEx123'

# class AuthenticationApiTests(TestCase):
#     '''Test the public features of the user API'''
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_new_user_successful(self):
#         '''test create new user successful'''
#         payload = {
#             'phone_number': phone_number_example,
#             'email': email_example,
#             'name': name_example,
#             'password': password_example,
#         }

#         res = self.client.post(USER_REGISTER_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)

#     def test_create_new_user_fields_failed(self):
#         '''test create failed user'''
#         pass

#     def test_create_user_existed(self):
#         '''test create existed user'''
#         pass

#     def test_create_user_receive_email_confirm(self):
#         '''test email confirm is sent when create new user'''
#         pass

#     def test_create_user_receive_OTP_confirm(self):
#         '''test OTP confirm is sent when create new user'''
#         pass