from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from app_todo import serializers
from knox.auth import TokenAuthentication
from core.models import (
    TodoCard,
    UserTodo,
)
from django.utils import timezone


class TodoCardViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = TodoCard.objects.all().order_by('updated_at')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TodoCardDetailSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    """
    note that any custom view will not call this func
    LOL : )
    """
    def get_queryset(self):
        user_todo = UserTodo.objects.get(
                user=self.request.user)
        queryset = self.queryset.filter(user_todo=user_todo)

        is_have_color_params: str = self.request.GET.get('is_have_color', None)
        is_done_params: str = self.request.GET.get('is_done', None)

        print('is_have_color***********', self.request)
        # print('is_done_params', is_done_params)

        if is_have_color_params is not None:
            queryset = queryset.filter(color__isnull=eval(is_have_color_params))
        if is_done_params is not None:
            queryset = queryset.filter(done_at__isnull=not eval(is_done_params))

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'sort-by-color']:
            return serializers.TodoCardSerializer
        if self.action == 'set_done_task_status':
            return serializers.RequestTodoCardStatusSerializer
        return self.serializer_class

    @action(
        methods=['PATCH'],
        detail=True,
        url_path='set-done',
        url_name='set-done')
    def set_done_task_status(self, request, pk=None):
        todo = self.get_object()
        serializer = serializers.RequestTodoCardStatusSerializer(
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

    @action(
        methods=['GET'],
        detail=False,
        url_path='sort-by-color',
        url_name='sort-by-color')
    def get_task_sort_by_color(self, request):
        user_todo = UserTodo.objects.get(user=request.user)
        queryset = self.queryset.filter(user_todo=user_todo)

        qr_param_is_done: str = self.request.query_params.get('is_done', None)

        if qr_param_is_done is not None:
            queryset = queryset.filter(
                done_at__isnull=not eval(qr_param_is_done))
        res = serializers.ResponseGetListByColor(queryset)
        return Response(
            data=res.data,
            status=status.HTTP_200_OK)
