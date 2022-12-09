from django.contrib.auth import get_user_model
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView
from user.utils import login_with_google_and_get_info
from user.serializers import (
    UserRegisterRequestSerializer,
    UserRegisterResponseSerializer,
)
from core.exceptions.exception_serializer import ExceptionSerializer


class LoginWithGoogle(KnoxLoginView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserRegisterRequestSerializer,
        responses={
            200: UserRegisterResponseSerializer,
            400: ExceptionSerializer, },
        description='Register new account to access the api',)
    def post(self, request, format=None):
        google_credential = request.data.get('credential')
        email, name = login_with_google_and_get_info(google_credential)
        user, is_new_user = get_user_model().objects.get_or_create(
            email=email, name=name
        )
        login(request, user)

        return super(LoginWithGoogle, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        """Custom response data when login via GG success"""
        UserSerializer = self.get_user_serializer_class()
        data = {'token': token}
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                    request.user,
                    context=self.get_context()).data
        return data
