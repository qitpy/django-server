from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from core.models import (
    TodoDaily,
    UserTodo)

from app_todo import serializers


class DailyViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = TodoDaily.objects.all().order_by('updated_at')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DailySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        user_todo = UserTodo.objects.get(
            user=self.request.user)
        queryset = self.queryset.filter(user_todo=user_todo)

        return queryset

    def get_serializer_class(self):
        if self.action == 'set_done_task_status':
            return serializers.RequestTodoDailyDoneStatusSerializer
        return self.serializer_class

    @action(
        methods=['PATCH'],
        detail=True,
        url_path='set-done',
        url_name='set-done')
    def set_done_task_status(self, request, pk=None):
        daily_todo = self.get_object()
        serializer = serializers.RequestTodoDailyDoneStatusSerializer(
            data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        daily_todo.done_at = timezone.now() \
            if serializer.data['is_done'] else \
            None
        daily_todo.save()
        data = serializers.DailySerializer(daily_todo)
        return Response(data.data, status=status.HTTP_200_OK)
