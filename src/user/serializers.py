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
        fields = ['email', 'name',]

    def create(self, validated_data):
        '''create and return a user with encrypted password'''
        user = get_user_model().objects.create_user(**validated_data)



        return user
