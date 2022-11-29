from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from app_todo import serializers
from knox.auth import TokenAuthentication
from core.models import (
    TodoCard,
    UserTodo
)
from django.utils import timezone


class TodoCardViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = TodoCard.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TodoCardDetailSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        user_todo = UserTodo.objects.get(
                user=self.request.user
            )
        return self.queryset.filter(
            user_todo=user_todo
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TodoCardSerializer
        if self.action == 'set_done_task_status':
            return serializers.TodoCardStatusSerializer
        return self.serializer_class

    @action(
        methods=['PATCH'],
        detail=True,
        url_path='set-done',
        url_name='set-done')
    def set_done_task_status(self, request, pk=None):
        todo = self.get_object()
        serializer = serializers.TodoCardStatusSerializer(
            data=request.data)
        if serializer.is_valid():
            if serializer.data['is_done']:
                todo.done_at = timezone.now()
            else:
                todo.done_at = None

            todo.save()
            data = serializers.TodoCardSerializer(todo).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
