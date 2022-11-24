from django.test import TestCase
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import PortfolioMessage

LEAVE_MESSAGE_URL = reverse('app_portfolio:leave-message-list')

good_payload = {
    'message': 'this is test message '
               'leave from user interface',
    'name_or_email': 'user name',
    'ip_address': '192.186.1.1',
}


class PublicPortfolioMessage(TestCase):
    """Test user leave message"""
    def setUp(self):
        self.client = APIClient()

    @patch('django.core.mail.send_mail')
    def test_user_leave_message_successful(self, patched_send_mail):
        patched_send_mail.return_value = 1
        res = self.client.post(LEAVE_MESSAGE_URL, good_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        portfolio_message = PortfolioMessage.objects.get(pk=res.data['id'])
        for key, value in good_payload.items():
            self.assertEqual(res.data[key], value)
            self.assertEqual(getattr(portfolio_message, key), value)

    @patch('django.core.mail.send_mail')
    def test_user_leave_message_failed_or_error(self, patched_send_mail):
        bad_payload_missing_ip: dict[str, str] = dict(
            message='this is test message leave from user interface',
            ip_address='This is really not a IP',
        )
        bad_payload_missing_message: dict[str, str] = dict(
            ip_address='192.186.1.2',
        )
        bad_ip_res = self.client.post(
            LEAVE_MESSAGE_URL, bad_payload_missing_ip)
        bad_message_res = self.client.post(
            LEAVE_MESSAGE_URL, bad_payload_missing_message)
        self.assertEqual(bad_ip_res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(bad_message_res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        patched_send_mail.assert_not_called()

    @patch('django.core.mail.send_mail')
    def test_limited_amount_of_message_in_one_minute(self, patched_send_mail):
        """user can not send too much message in a time
        - maximum 3 message in a minutes"""
        payload = {
            'message': 'this is test message '
                       'from testing',
            'name_or_email': 'user name',
            'ip_address': '192.186.21.10',
        }
        patched_send_mail.side_effect = [1] * 4
        first_res = self.client.post(
            LEAVE_MESSAGE_URL, payload
        )
        second_res = self.client.post(
            LEAVE_MESSAGE_URL, payload
        )
        third_res = self.client.post(
            LEAVE_MESSAGE_URL, payload
        )
        self.assertEqual(first_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(third_res.status_code, status.HTTP_201_CREATED)

        four_res = self.client.post(
            LEAVE_MESSAGE_URL, payload
        )
        self.assertEqual(four_res.status_code, status.HTTP_400_BAD_REQUEST)
