from rest_framework import serializers
from core.models import (
    TodoCard,
    UserTodo,
)


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


class TodoCardDetailSerializer(TodoCardSerializer):
    class Meta(TodoCardSerializer.Meta):
        fields = TodoCardSerializer.Meta.fields + ['created_at', 'updated_at']
        read_only_fields = TodoCardSerializer.Meta.read_only_fields \
            + ['created_at', 'updated_at']


class RequestTodoCardStatusSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=True)


class ResponseGetListByColor(serializers.Serializer):

    def to_representation(self, internal_data):
        deserialize_data = TodoCardSerializer(
            internal_data, many=True).data

        task_sorted_by_pink = filter(
            lambda x: x['color'] == TodoCard.TodoCardColor.PINK,
            deserialize_data)
        task_sorted_by_orange = filter(
            lambda x: x['color'] == TodoCard.TodoCardColor.ORANGE,
            deserialize_data)
        task_sorted_by_blue = filter(
            lambda x: x['color'] == TodoCard.TodoCardColor.BLUE,
            deserialize_data)
        task_sorted_by_green = filter(
            lambda x: x['color'] == TodoCard.TodoCardColor.GREEN,
            deserialize_data)

        instance = {}
        instance['pink_task'] = list(task_sorted_by_pink)
        instance['orange_task'] = list(task_sorted_by_orange)
        instance['blue_task'] = list(task_sorted_by_blue)
        instance['green_task'] = list(task_sorted_by_green)

        return instance
