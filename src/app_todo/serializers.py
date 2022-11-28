from rest_framework import serializers
from core.models import (
    TodoCard,
    UserTodo,
)


class TodoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCard
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

    def create(self, validate_data):
        user = self.context['request'].user
        user_todo, _ = UserTodo.objects.get_or_create(user=user)
        todo_card = TodoCard.objects.create(
            user_todo=user_todo,
            **validate_data)
        return todo_card
