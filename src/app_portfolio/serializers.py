from rest_framework import serializers
from core.models import (
    PortfolioMessage,
    PortfolioAccessFrequency,
)
from django.core.mail import send_mail

import re


class PortfolioAccessFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAccessFrequency
        fields = ['id', 'ip_address']
        read_only_fields = ['id']


def send_notify_email(message: PortfolioMessage):
    message_template = f'from {message.name_or_email},\n' \
                       f'{message.message},\n' \
                       f'{message.created_at},\n' \
                       f'{message.ip_address}'
    send_mail(
        'Portfolio Message',
        message_template,
        'maitocode@gmail.com',
        ['code.maito@gmail.com'],
        fail_silently=False,
    )


class PortfolioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioMessage
        fields = ['id', 'message', 'name_or_email', 'ip_address']
        read_only_fields = ['id']

    def validate(self, data):
        """validate IP address after validate fields"""
        pattern = re.compile(r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)"
                             r"{3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])")
        if not re.fullmatch(pattern, data['ip_address']):
            raise serializers.ValidationError('is not IP address', code='400')
        return data

    def create(self, validated_data):
        """send email when someone message me"""
        message = PortfolioMessage.objects.create(**validated_data)
        send_notify_email(message=message)
        return message
