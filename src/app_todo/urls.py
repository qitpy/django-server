from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_todo import views

app_name = 'app_todo'

router = DefaultRouter()
router.register('todo-card',
                views.TodoCardViewSet,
                basename='todo_card')

urlpatterns = [
    path('', include(router.urls))
]