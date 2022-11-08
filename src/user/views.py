from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from requests.exceptions import HTTPError
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import serializers
import os


class LoginWithGoogle(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = None
        name = None
        try:
            google_credential = request.data.get('credential')
            CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID'),
            user_info = id_token.verify_oauth2_token(
                google_credential, requests.Request(), CLIENT_ID
            )
            email = user_info['email']
            name = user_info['name']
        except ValueError:
            return Response(
                {
                    'errors': {
                        'token': 'Invalid token'
                        }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, is_new_user = get_user_model().objects.get_or_create(
            email=email, name=name
        )
        if not is_new_user:
            user.auth_token_set.all().delete()

        login(request, user)
        return super(LoginWithGoogle, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def authentication_test(request):
    print(request.user)
    return Response(
        {
            'message': "User successfully authenticated"
        },
        status=status.HTTP_200_OK,
    )