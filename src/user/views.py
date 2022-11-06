from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from requests.exceptions import HTTPError
from knox.models import AuthToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView


class LoginWithGoogle(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = None
        name = None
        try:
            google_credential = request.data.get('credential')
            CLIENT_ID = '451670753998-ct3drfnm9ote4v5b03b4s0aa3206l64p.apps.googleusercontent.com'
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
        login(request, user)
        return super(LoginWithGoogle, self).post(request, format=None)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_by_access_token(request, backend):
#     email = None
#     name = None
#     try:
#         # Specify the CLIENT_ID of the app that accesses the backend:
#         google_credential = request.data.get('credential')
#         CLIENT_ID = '451670753998-ct3drfnm9ote4v5b03b4s0aa3206l64p.apps.googleusercontent.com'
#         user_info = id_token.verify_oauth2_token(
#             google_credential, requests.Request(), CLIENT_ID
#         )

#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')

#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')

#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         email = user_info['email']
#         name = user_info['name']
#     except ValueError:
#         # Invalid token
#         return Response(
#             {
#                 'errors': {
#                     'token': 'Invalid token'
#                     }
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     user, is_new_user = get_user_model().objects.get_or_create(
#         email=email, name=name
#     )

#     login(request, user)

#     token, created = AuthToken.objects.get_or_create(user=user)
#     return Response(
#         {
#             'token': token,
#             'created': created,
#         },
#         status=status.HTTP_200_OK,
#         )


@api_view(['GET', 'POST'])
def authentication_test(request):
    print(request.user)
    return Response(
        {
            'message': "User successfully authenticated"
        },
        status=status.HTTP_200_OK,
    )