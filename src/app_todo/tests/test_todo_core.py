from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    TodoCard,
)

TODO_CARD_URL = reverse('app_todo:todo_card-list')


def update_todo_status_url(todo_id):
    return reverse('app_todo:todo_card-set-done', args=[todo_id])


def todo_card_detail_url(pk):
    """create and return todo_card detail URL"""
    return reverse('app_todo:todo_card-detail', args=[pk])


def create_user(email='quyet.doan@gmail.com', name='Quiet'):
    """create and return a new user"""
    return get_user_model().objects.create_user(email, name)


class PublicTodoCardApiTest(TestCase):
    """test unauthenticated API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TODO_CARD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoCardApiTest(TestCase):
    """test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_todo_card_create_api_successful(self):
        """test create todo_card successful"""
        payload = {
            'name': 'todo task name',
            'description': 'descriptions of the task',
        }
        res = self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['done_at'], None)
        todo_card_id = res.data['id']
        todo_card = TodoCard.objects.get(pk=todo_card_id)
        for key, value in payload.items():
            self.assertEqual(getattr(todo_card, key), value)
        self.assertTrue(todo_card.user_todo.user_id == self.user.id)

    def test_todo_card_create_api_failed(self):
        """test create case failed when create todo_card"""
        payload = {
            'name': '',
            'description': ''
        }
        res = self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            'description': ''
        }
        self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {}
        self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_todo_card_successful(self):
        """test update todo_card that will be success"""
        payload_init = {
            'name': 'this is my task',
            'description': 'this is my description on my task'
        }
        payload_update = {
            'name': 'this is the task updated',
            'description': 'this is my the updating of the description'
        }
        res = self.client.post(TODO_CARD_URL, payload_init)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        todo_card_id = res.data['id']
        res_patch = self.client.patch(
          todo_card_detail_url(pk=todo_card_id),
          payload_update
        )
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_patch.data['done_at'], None)
        todo_card_updated = TodoCard.objects.get(pk=todo_card_id)
        for key, value, in payload_update.items():
            self.assertEqual(getattr(todo_card_updated, key), value)

    def test_set_todo_card_status(self):
        payload_todo_card = {
            'name': 'this is my task',
            'description': 'this is my description on my task'
        }
        payload_done = {
            'is_done': True
        }
        payload_not_done = {
            'is_done': False
        }
        res_init_card = self.client.post(TODO_CARD_URL, payload_todo_card)
        self.assertEqual(res_init_card.status_code, status.HTTP_201_CREATED)

        todo_card = TodoCard.objects.get(pk=res_init_card.data['id'])
        res_set_status_done = self.client.patch(
            update_todo_status_url(
                res_init_card.data['id']
            ),
            payload_done
        )
        self.assertEqual(res_set_status_done.status_code, status.HTTP_200_OK)

        todo_card.refresh_from_db()
        self.assertNotEqual(todo_card.done_at, None)
        self.assertNotEqual(res_set_status_done.data['done_at'], None)

        res_set_status_not_done = self.client.patch(
            update_todo_status_url(
                res_init_card.data['id'],
            ),
            payload_not_done
        )
        self.assertEqual(
            res_set_status_not_done.status_code,
            status.HTTP_200_OK)

        todo_card.refresh_from_db()
        self.assertEqual(todo_card.done_at, None)
        self.assertEqual(res_set_status_not_done.data['done_at'], None)

    # def test_get_todo_card_detail(self):
    #     payload_create_todo_card = {

    #     }
