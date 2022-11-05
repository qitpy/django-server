'''
Views for the user API
'''
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from user.serializers import (
    UserSerializer,
    LoginUserSerializer,
)

class RegisterUserView(generics.CreateAPIView):
    '''Create a new user in the system'''
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    '''Login user return a token'''
    serializer_class = LoginUserSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''Manage the authenticated user'''
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''retrieve and return the authenticated user'''
        return self.request.user

@api_view(['GET'])
def VerifyEmailView(request):
    '''Verify email view'''
    params = request.query_params
    email = params['email']
    verify_email_code = params['code']
    user = get_user_model().objects.get(email=email)

    if user:
        if user.verify_email_code is verify_email_code:
            return Response(
                {"message": "you successfully verify your email"},
                status=status.HTTP_200_OK,
            )
    return Response(
        {"message": "this link is expired or something wrong, \
            please re-confirm your email by request to \
                send confirm email again"},
        status=status.HTTP_400_BAD_REQUEST,
    )
