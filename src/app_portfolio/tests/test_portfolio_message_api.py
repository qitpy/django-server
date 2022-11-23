from django.test import TestCase
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import PortfolioMessage

LEAVE_MESSAGE_URL = reverse('app_portfolio:leave-message-list')


class PublicPortfolioMessage(TestCase):
    """Test user leave message"""
    def setUp(self):
        self.client = APIClient()

    @patch('django.core.mail.send_mail')
    def test_user_leave_message_successful(self, patched_send_mail):
        patched_send_mail.return_value = 1
        payload = {
            'message': 'this is test message '
                       'leave from user interface',
            'name_or_email': 'user name',
            'ip_address': '192.186.1.1',
        }
        print(LEAVE_MESSAGE_URL)
        res = self.client.post(LEAVE_MESSAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        portfolio_message = PortfolioMessage.objects.get(pk=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(res.data[key], value)
            self.assertEqual(getattr(portfolio_message, key), value)

    @patch('django.core.mail.send_mail')
    def test_user_leave_message_failed_or_error(self, patched_send_mail):
        bad_payload_bad_ip: dict[str, str] = dict(
            message='this is test message leave from user interface',
            ip_address='This is really not a IP',
        )
        bad_payload_bad_message: dict[str, str] = dict(
            ip_address='192.186.1.2',
        )
        bad_ip_res = self.client.post(
            LEAVE_MESSAGE_URL, bad_payload_bad_ip)
        bad_message_res = self.client.post(
            LEAVE_MESSAGE_URL, bad_payload_bad_message)
        self.assertEqual(bad_ip_res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(bad_message_res.status_code,
                         status.HTTP_400_BAD_REQUEST)
        patched_send_mail.assert_not_called()
