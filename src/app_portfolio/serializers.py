from rest_framework import serializers
from core.models import (
    PortfolioMessage,
    PortfolioAccessFrequency,
)
from django.core.mail import send_mail


class PortfolioAccessFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAccessFrequency
        fields = ['ip_address']


def send_notify_email(message: PortfolioMessage):
    message_template = f'from {message.name_or_email},\n' \
                       f'{message.message},\n' \
                       f'{message.created_at},\n' \
                       f'{message.ip_address}'
    send_mail(
        'Portfolio Message',
        message_template,
        'maitoserver@gmail.com',
        ['code.maito@gmail.com'],
        fail_silently=False,
    )


class PortfolioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioMessage
        fields = ['message', 'name_or_email', 'ip_address']

    def create(self, validated_data):
        """send email when someone message me"""
        message = PortfolioMessage.objects.create(**validated_data)
        send_notify_email(message=message)
        return message
