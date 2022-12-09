from rest_framework import serializers
from core.models import (
    TodoCard,
    UserTodo,
)
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)
from app_todo.utils import (
    separate_to_tasks_by_color_from_serialize_data,
)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'response detail',
            description='',
            value={
                "id": 0,
                "name": "swim tonight",
                "color": "HT",
                "description": "swim with Peter & Dough",
                "done_at": "2022-12-08T09:39:47.454Z",
            },
            response_only=True, ), ])
class TodoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCard
        fields = [
            'id',
            'name',
            'description',
            'color',
            'done_at']
        read_only_fields = ['id', 'done_at']

    def create(self, validate_data):
        user = self.context['request'].user
        user_todo, _ = UserTodo.objects.get_or_create(user=user)
        todo_card = TodoCard.objects.create(
            user_todo=user_todo,
            **validate_data)
        return todo_card

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'response example',
            description='',
            value={
                "id": 0,
                "name": "swim tonight",
                "description": "swim with Peter & Dough",
                "color": "HT",
                "done_at": "2022-12-08T09:39:47.454Z",
                "created_at": "2022-12-08T09:39:47.454Z",
                "updated_at": "2022-12-08T09:39:47.454Z"
            },
            response_only=True,),
        OpenApiExample(
            'request example',
            description='',
            value={
                "name": "swim tonight",
                "description": "swim with Peter & Dough",
                "color": "HT",
            },
            request_only=True, ), ])
class TodoCardDetailSerializer(TodoCardSerializer):
    class Meta(TodoCardSerializer.Meta):
        fields = TodoCardSerializer.Meta.fields + ['created_at', 'updated_at']
        read_only_fields = TodoCardSerializer.Meta.read_only_fields \
            + ['created_at', 'updated_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'set task done',
            description='',
            value={'is_done': True},
            request_only=True,),
        OpenApiExample(
            'set task not done yet',
            description='',
            value={'is_done': False},
            request_only=True, ), ])
class RequestTodoCardStatusSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=True)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'set task done',
            description='',
            value={
                'pink_task': [{
                    "id": 1,
                    "name": "some task",
                    "description": "some task",
                    "color": "HT",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, {
                    "id": 2,
                    "name": "some task",
                    "description": "some task",
                    "color": "HT",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, ],
                'orange_task': [{
                    "id": 3,
                    "name": "some task",
                    "description": "some task",
                    "color": "H",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, {
                    "id": 4,
                    "name": "some task",
                    "description": "some task",
                    "color": "H",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, ],
                'blue_task': [{
                    "id": 5,
                    "name": "some task",
                    "description": "some task",
                    "color": "L",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, {
                    "id": 6,
                    "name": "some task",
                    "description": "some task",
                    "color": "L",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, ],
                'green_task': [{
                    "id": 7,
                    "name": "some task",
                    "description": "some task",
                    "color": "LT",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, {
                    "id": 8,
                    "name": "some task",
                    "description": "some task",
                    "color": "LT",
                    "done_at": "2022-12-08T10:33:12.417Z"
                }, ],
            },
            response_only=True, ), ])
class ResponseGetListByColor(serializers.Serializer):

    pink_task = TodoCardDetailSerializer(many=True)
    orange_task = TodoCardDetailSerializer(many=True)
    blue_task = TodoCardDetailSerializer(many=True)
    green_task = TodoCardDetailSerializer(many=True)

    def to_representation(self, internal_data: list[TodoCard]):
        """
        internal_data: serialized data get from database
        """
        deserialize_data = TodoCardSerializer(
            internal_data, many=True).data
        instance = \
            separate_to_tasks_by_color_from_serialize_data(
                deserialize_data)

        return instance
