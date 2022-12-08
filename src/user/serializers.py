"""
serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        user = get_user_model().objects.create_user(**validated_data)

        return user


@extend_schema_serializer(
    examples=[
         OpenApiExample(
            'Google credential',
            summary='The credential key',
            description='your Google credential key that get from response\
                after login success',
            value={
                'credential': '0uuSAtBcMzR5ef2YizE5OB4ILHKFMSmejU71CzZq',
            },
            request_only=True, ), ])
class UserRegisterRequestSerializer(serializers.Serializer):
    credential = serializers.CharField(
        max_length=200,
        help_text='0uuSAtBcMzR5ef2YizE5OB4ILHKFMSmejU71CzZq')


@extend_schema_serializer(
    examples=[
         OpenApiExample(
            'Google credential',
            summary='The credential key',
            description='your Google credential key that get\
                from response after login success',
            value={
                "user": {
                    "email": "user@example.com",
                    "name": "user name"
                },
                "session_token": "OTfcxfN243sFVbuCaPZ3EPpk0GV\
                    NJMe9HJjxX5zIXybjJ4aLls"
            },
            response_only=True, ), ])
class UserRegisterResponseSerializer(serializers.Serializer):
    user = UserSerializer(many=False, required=True)
    session_token = serializers.CharField(max_length=200,)
