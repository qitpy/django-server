'''
serializers for the user API View
'''
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

import re


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the user object'''

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password',]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            }
        }

    def create(self, validated_data):
        '''create and return a user with encrypted password'''

        if not re.fullmatch('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}', password):
            raise ValueError('Password must be have at least ' \
                + 'one normal character, ' \
                + 'one uppercase characters ' \
                + 'and one number')

        # send token sdt

        # send token email

        return get_user_model().objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    '''serializer for the user auth token'''