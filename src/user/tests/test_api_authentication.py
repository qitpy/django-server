# '''
# test user register, login, token authentication
# '''
#
# from unittest.mock import patch
# from django.test import TestCase
# from django.core import mail
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from core.models import (
#     User,
# )
#
# USER_REGISTER_URL = reverse('user:register')
# USER_LOGIN_URL = reverse('user:login')
#
#
# def user_verify_email_url(query_params):
#     '''create and return verify email request url'''
#     return reverse('user:verify-email', args=[query_params])
#
#
# email_example = 'email@yopmail.com'
# name_example = 'username example'
# password_example = 'PasswordEx123'
#
#
# def create_user(email=email_example,
#                 name=name_example,
#                 password=password_example):
#     '''create and return a new user'''
#     return get_user_model().objects.create_user(
#         email, name, password
#     )
#
#
# class AuthenticationApiTests(TestCase):
#     '''Test the public features of the user API'''
#
#     def setUp(self):
#         self.client = APIClient()
#
#     @patch('django.core.mail.send_mail')
#     def test_create_new_user_successful(self, patched_mail):
#         '''test create new user successful'''
#         patched_mail.return_value = 1
#         payload = {
#             'email': email_example,
#             'name': name_example,
#             'password': password_example,
#         }
#
#         res = self.client.post(USER_REGISTER_URL, payload)
#         user = User.objects.get(email=email_example)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(user.name, payload['name'])
#         self.assertTrue(user.check_password(payload['password']))
#
#     def test_create_user_existed(self):
#         '''test create existed user'''
#         create_user()
#         payload = {
#             'email': email_example,
#             'name': name_example,
#             'password': password_example,
#         }
#         res = self.client.post(USER_REGISTER_URL, payload)
#
#         self.assertEqual(res.status_code, 400)
#
#     def test_create_user_sent_email_confirm(self):
#         '''test email confirm is sent when create new user'''
#         payload = {
#             'email': email_example,
#             'name': name_example,
#             'password': password_example,
#         }
#         res = self.client.post(USER_REGISTER_URL, payload)
#
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].recipients[0], email_example)
#
#     @patch('core.models.UserManager.random_verify_email_code')
#     def test_create_user_confirm_successfully(
#             self,
#             patched_verify_email_code_random
#     ):
#         '''test that user verify email successfully'''
#         verify_email_code = 'THISisVERIFYcodeFORemailVERIFYING'
#         patched_verify_email_code_random.return_value = verify_email_code
#         user = create_user()
#         payload = {
#             'email': email_example,
#             'password': password_example
#         }
#         res = self.client.post(USER_LOGIN_URL, payload)
#         self.assertEqual(res.status_code, 403)
#
#         query_params = {
#             'email': email_example,
#             'code': verify_email_code,
#         }
#         res_verify_email = self.client.get(
#             user_verify_email_url(query_params)
#         )
#         user.refresh_from_db()
#         self.assertEqual(res_verify_email.status_code, 200)
#         self.assertTrue(user.is_active)
#         res = self.client.post(USER_LOGIN_URL, payload)
#         self.assertEqual(res.status_code, 200)
#
#     @patch('core.models.UserManager.random_verify_email_code')
#     @patch('user.utils.is_expired_verify_email_code')
#     def test_time_confirm_email_expired(
#             self, patched_verify_email_code, patched_expired_verify_email):
#         '''
#         test time confirm email will be expired in 10min
#         user need to resend confirm email to verify
#         '''
#         verify_email_code = 'THISisVERIFYcodeFORemailVERIFYING'
#         patched_verify_email_code.return_value = verify_email_code
#         patched_expired_verify_email.return_value = True
#         create_user()
#         query_params = {
#             'email': email_example,
#             'code': verify_email_code,
#         }
#         res_verify_email = self.client.get(
#             user_verify_email_url(query_params)
#         )
#
#         self.assertEqual(res_verify_email.status_code, 400)
#
#     @patch('core.models.UserManager.random_verify_email_code')
#     def test_login_failed_10_time_will_be_block(
#             self, patched_verify_email_code_random
#     ):
#         '''
#         test that will block account in case user attempt
#         to input many time password, for security
#         '''
#         verify_email_code = 'THISisVERIFYcodeFORemailVERIFYING'
#         patched_verify_email_code_random.return_value = verify_email_code
#         email = 'attempt@yopmail.com'
#         user = create_user(email=email)
#         payload_wrong_password = {
#             'email': email,
#             'password': 'wrong' + password_example,
#         }
#         payload_true_password = {
#             'email': email,
#             'password': password_example,
#         }
#         query_params = {
#             'email': email_example,
#             'code': verify_email_code,
#         }
#         res_verify_email = self.client.get(
#             user_verify_email_url(query_params)
#         )
#         self.assertEqual(res_verify_email.status_code, 200)
#
#         res_true = self.client.post(USER_LOGIN_URL, payload_true_password)
#         self.assertEqual(res_true.status_code, 200)
#         user.refresh_from_db()
#         self.assertEqual(user.password_attempt_times, 0)
#
#         for i in range(10):
#             res_wrong = self.client.post(
#                 USER_LOGIN_URL, payload_wrong_password
#             )
#             self.assertEqual(res_wrong, 401)
#
#         user.refresh_from_db()
#         self.assertEqual(user.password_attempt_times, 10)
#         res_true = self.client.post(USER_LOGIN_URL, payload_true_password)
#         self.assertEqual(res_true.status_code, 401)
