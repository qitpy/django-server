from django.conf import settings
from django.db import models


class TodoCardBase(models.Model):
    """task in short time"""

    class Meta:
        abstract = True

    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    is_done = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done_at = models.DateTimeField(blank=True, null=True)


class UserTodo(models.Model):
    """Connection between user & Todo App"""

    class Meta:
        db_table = 'todo_user'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    weekly_note = models.TextField(
        blank=True,
        null=True,
        default='there are no note',
    )

    def __str__(self):
        return "asaaaa"


class TodoDaily(TodoCardBase):
    class Meta:
        db_table = 'todo_daily'

    user_todo = models.ForeignKey(
        UserTodo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class TodoSchedule(TodoCardBase):
    """task that is scheduled"""

    class Meta:
        db_table = 'todo_schedule'

    expired_time = models.DateTimeField(blank=False, null=False)
    note = models.TextField(blank=True, null=True)

    user_todo = models.ForeignKey(
        UserTodo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class TodoCard(TodoCardBase):
    class Meta:
        db_table = 'todo_cards'

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
    user_todo = models.ForeignKey(
        UserTodo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class TodoMonth(TodoCardBase):
    """Task in Month"""

    class Meta:
        db_table = 'todo_month'

    month_name = models.CharField(max_length=255, null=False, blank=False)
    child_task = models.ManyToManyField(TodoCard)

    user_todo = models.ForeignKey(
        UserTodo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class TodoYear(TodoCardBase):
    """Task in Month"""

    class Meta:
        db_table = 'todo_year'

    month_todo = models.ManyToManyField(TodoMonth)
    child_task = models.ManyToManyField(TodoCard)

    user_todo = models.ForeignKey(
        UserTodo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
