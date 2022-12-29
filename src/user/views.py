from django.contrib.auth import get_user_model
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView
from user.utils import UserUtils
from user.serializers import (
    UserRegisterRequestSerializer,
    UserRegisterResponseSerializer,
)
from core.exceptions.exception_serializer import ExceptionSerializer
from core.models import User
from user.serializers import UserSerializer


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
        email, name = \
            UserUtils.login_with_google_and_get_info(google_credential)
        user, _ = get_user_model().objects.get_or_create(
            email=email, name=name
        )
        login(request, user)

        return super(LoginWithGoogle, self).post(request, format=None)

    def get_post_response_data(self, request, token, _):
        """Custom response data when login via GG success"""
        data = {'token': token}
        user = User.objects.get(email=request.user)
        data["user"] = UserSerializer(user).data
        return data
