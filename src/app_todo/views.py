from rest_framework import viewsets, mixins
from app_todo import serializers
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class TodoCardViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TodoCardSerializer