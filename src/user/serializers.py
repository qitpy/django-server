'''
serializers for the user API View
'''
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        user = get_user_model().objects.create_user(**validated_data)

        return user


class UserRegisterRequestSerializer(serializers.Serializer):
    credential = serializers.CharField(max_length=200,)


class UserRegisterResponseSerializer(serializers.Serializer):
    user = UserSerializer(many=False, required=True)
    session_token = serializers.CharField(max_length=200,)
