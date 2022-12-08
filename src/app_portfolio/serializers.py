from rest_framework import serializers
from core.models import (
    PortfolioMessage,
    PortfolioAccessFrequency,
)
from app_portfolio.utils import (
    send_notify_email,
    validate_limit_message_in_a_minutes,
    validate_ip_address,
)
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'body',
            description='save user IP to server',
            value={"ip_address": "121.115.32.142"},
            request_only=True,),
        OpenApiExample(
            'body',
            description='',
            value={
                "id": 0,
                "ip_address": "121.115.32.142"},
            response_only=True, ), ])
class PortfolioAccessFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAccessFrequency
        fields = ['id', 'ip_address']
        read_only_fields = ['id']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'body',
            description='save user IP to server',
            value={
                "message": "hello, this is message from someone special",
                "name_or_email": "secret",
                "ip_address": "121.115.32.142"},
            request_only=True,),
        OpenApiExample(
            'body',
            description='',
            value={
                "id": 0,
                "message": "hello, this is message from someone special",
                "name_or_email": "secret",
                "ip_address": "121.115.32.142"},
            response_only=True, ), ])
class PortfolioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioMessage
        fields = ['id', 'message', 'name_or_email', 'ip_address']
        read_only_fields = ['id']

    def validate(self, data):
        """validate IP address after validate fields"""
        if not validate_ip_address(data['ip_address']):
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
