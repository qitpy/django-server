from django.conf import settings
from django.db import models


class TodoCard(models.Model):
    """task in short time"""

    class Meta:
        db_table = 'todo_card'

    class TodoCardColor(models.TextChoices):
        PINK = 'HT', 'HIGHEST'
        ORANGE = 'H', 'HIGH'
        BLUE = 'L', 'LOW'
        GREEN = 'LT', "LOWEST"

    color = models.CharField(
        max_length=2,
        choices=TodoCardColor.choices,
        null=True
    )

    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    is_done = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done_at = models.DateTimeField(blank=True, null=True)


class TodoMonth(models.Model):
    """Task in Month"""
    class Meta:
        db_table = 'todo_month'

    name = models.TextField(blank=False, null=False)
    tasks = models.ForeignKey(
        TodoCard,
        on_delete=models.CASCADE
    )


class TodoYear(models.Model):
    """Task in Month"""
    class Meta:
        db_table = 'todo_year'

    name = models.TextField(blank=False, null=False)
    tasks = models.ForeignKey(TodoCard, on_delete=models.CASCADE)
    month_tasks = models.ForeignKey(TodoMonth, on_delete=models.CASCADE)


class TodoSchedule(models.Model):
    """task that is scheduled"""
    class Meta:
        db_table = 'todo_schedule'
    expired_time = models.DateTimeField(blank=False, null=False)
    note = models.TextField(blank=True, null=True)
    task = models.OneToOneField(
        TodoCard,
        on_delete=models.CASCADE
    )


class UserTodo(models.Model):
    """Connection between user & Todo App"""
    class Meta:
        db_table = 'todo_user'
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tasks = models.ForeignKey(
        TodoCard,
        on_delete=models.CASCADE
    )
    tasks_months = models.ForeignKey(
        TodoMonth,
        on_delete=models.CASCADE
    )
    tasks_year = models.ForeignKey(
        TodoYear,
        on_delete=models.CASCADE
    )
    weekly_note = models.TextField(
        blank=True,
        null=True,
        default='there are no note'
    )
    daily_tasks = models.ForeignKey(
        TodoCard,
        on_delete=models.CASCADE,
        related_name='daily'
    )
    schedule_tasks = models.ForeignKey(
        TodoSchedule,
        on_delete=models.CASCADE
    )
