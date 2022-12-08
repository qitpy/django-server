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
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema_view
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "is_done",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY),
            OpenApiParameter(
                "is_have_color",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY),
        ], ))
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

    def get_queryset(self):
        user_todo = UserTodo.objects.get(
                user=self.request.user)
        queryset = self.queryset.filter(user_todo=user_todo)

        is_have_color_params: str = self.request.GET.get('is_have_color', None)
        is_done_params: str = self.request.GET.get('is_done', None)

        if is_have_color_params is not None:
            queryset = queryset.filter(
                color__isnull=not eval(is_have_color_params))
        if is_done_params is not None:
            queryset = queryset.filter(
                done_at__isnull=not eval(is_done_params))

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'sort-by-color']:
            return serializers.TodoCardSerializer
        if self.action == 'set_done_task_status':
            return serializers.RequestTodoCardStatusSerializer
        return self.serializer_class

    @extend_schema(
        request=serializers.RequestTodoCardStatusSerializer,
        responses={200: serializers.TodoCardSerializer})
    @action(
        methods=['PATCH'],
        detail=True,
        url_path='set-done',
        url_name='set-done')
    def set_done_task_status(self, request, pk=None):
        todo = self.get_object()
        serializer = serializers.RequestTodoCardStatusSerializer(
            data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        todo.done_at = timezone.now() \
            if serializer.data['is_done'] else \
            None
        todo.save()
        data = serializers.TodoCardSerializer(todo)
        return Response(data.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_done",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY), ],
        request=None,
        responses={200: serializers.ResponseGetListByColor, })
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
