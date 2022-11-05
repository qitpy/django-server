'''
serializers for the user API View
'''
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

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
        password = validated_data.get('password')
        if not re.fullmatch('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}', password):
            raise ValueError('Password must be have at least ' \
                + 'one normal character, ' \
                + 'one uppercase characters ' \
                + 'and one number')

        user = get_user_model().objects.create_user(**validated_data)
        subject = 'test send mail'
        email_from = settings.EMAIL_HOST_USER
        message = 'HiHi'
        recipient_list = [user.email,]
        send_mail(subject, message, email_from, recipient_list)
        return user


class LoginUserSerializer(serializers.Serializer):
    '''serializer for the user auth token'''