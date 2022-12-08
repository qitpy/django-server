from rest_framework import serializers
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
)


@extend_schema_serializer(
    examples=[
         OpenApiExample(
            'Google credential',
            summary='The credential key',
            description='your Google credential key that get from\
                response after login success',
            value={
                "status_code": 400,
                "default_detail": "some error detail",
                "default_code": "error_code"
            },
            response_only=True, ), ])
class ExceptionSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(default=400)
    default_detail = serializers.CharField(default='some error detail')
    default_code = serializers.CharField(default='error_code')
