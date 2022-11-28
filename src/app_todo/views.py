from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
from app_todo import serializers
from knox.auth import TokenAuthentication
from core.models import (
    TodoCard,
    UserTodo
)


class TodoCardViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = TodoCard.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TodoCardSerializer

    def get_queryset(self):
        user_todo = UserTodo.objects.get(
                user=self.request.user
            )
        return self.queryset.filter(
            user_todo=user_todo
        )

    # @action(methods=['PATCH'], detail=True, url_path='set-done')
    # def set_done_task_status(self, request, pk=None):
    #     todo = self.get_object()
