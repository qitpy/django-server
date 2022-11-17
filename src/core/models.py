from django.conf import settings
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, name):
        """create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        """create and return a new superuser"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False, unique=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


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




