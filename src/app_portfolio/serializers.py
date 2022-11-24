from rest_framework import serializers
from core.models import (
    PortfolioMessage,
    PortfolioAccessFrequency,
)
from app_portfolio.utils import (
    send_notify_email,
    validate_limit_message_in_a_minutes
)

import re


class PortfolioAccessFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAccessFrequency
        fields = ['id', 'ip_address']
        read_only_fields = ['id']


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
        if not validate_limit_message_in_a_minutes(data['ip_address']):
            raise serializers.ValidationError(
                "it's seem like spam - too much message in a minute")
        return data

    def create(self, validated_data):
        """send email when someone message me"""
        message = PortfolioMessage.objects.create(**validated_data)
        send_notify_email(message=message)
        return message
