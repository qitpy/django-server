from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    TodoCard,
)

import datetime

TODO_CARD_URL = reverse('app_todo:todo_card-list')


def update_todo_status_url(todo_id):
    return reverse('app_todo:todo_card-set-done', args=[todo_id])


def todo_card_detail_url(pk):
    """create and return todo_card detail URL"""
    return reverse('app_todo:todo_card-detail', args=[pk])


def create_user(email='quyet.doan@gmail.com', name='Quiet'):
    """create and return a new user"""
    return get_user_model().objects.create_user(email, name)


payload_create_todo_card_default = {
    'name': 'todo task name test',
    'description': 'descriptions of the task test',
}

timezone_field = ['updated_at', 'created_at', 'done_at']


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
        # test response is valid
        res = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['done_at'], None)
        self.assertEqual(res.data['color'], None)
        self.assertNotEqual(res.data['created_at'], None)
        self.assertNotEqual(res.data['updated_at'], None)

        # test payload with database valid
        todo_card_id = res.data['id']
        todo_card = TodoCard.objects.get(pk=todo_card_id)
        for key, value in payload_create_todo_card_default.items():
            self.assertEqual(res.data[key], value)
        self.assertTrue(todo_card.user_todo.user_id == self.user.id)

        # test response with database valid
        for key, value in res.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_card, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(getattr(todo_card, key), value)

    def test_todo_card_create_api_failed(self):
        """test create case failed when create todo_card"""
        # value is not blank at field 'name'
        payload = {
            'name': '',
            'description': ''
        }
        res = self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST)

        # 'name' is required
        payload = {
            'description': 'test description'
        }
        payload_empty = {}
        self.client.post(TODO_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.post(TODO_CARD_URL, payload_empty)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_todo_card_successful(self):
        """test update todo_card that will be success"""
        # create todo_card
        payload_update = {
            'name': 'this is the task updated',
            'description': 'this is my the updating of the description'
        }
        res = self.client.post(TODO_CARD_URL, payload_create_todo_card_default)
        todo_card_id = res.data['id']
        res_patch = self.client.patch(
          todo_card_detail_url(pk=todo_card_id),
          payload_update
        )
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_patch.data['done_at'], None)
        todo_card_updated = TodoCard.objects.get(pk=todo_card_id)

        # check payload with database is the same data
        for key, value, in payload_update.items():
            self.assertEqual(getattr(todo_card_updated, key), value)

        # test response with database valid
        for key, value in res_patch.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_card_updated, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(getattr(todo_card_updated, key), value)

    def test_set_todo_card_status(self):
        payload_done = {
            'is_done': True
        }
        payload_not_done = {
            'is_done': False
        }
        res_init_card = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        todo_card = TodoCard.objects.get(pk=res_init_card.data['id'])

        # test done task
        res_set_status_done = self.client.patch(
            update_todo_status_url(res_init_card.data['id']),
            payload_done)
        todo_card.refresh_from_db()
        self.assertEqual(
            res_set_status_done.status_code,
            status.HTTP_200_OK)
        self.assertNotEqual(
            todo_card.done_at,
            None)
        self.assertNotEqual(
            res_set_status_done.data['done_at'],
            None)
        for key, value in res_set_status_done.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_card, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo_card, key),
                    value)

        # test not done task
        res_set_status_not_done = self.client.patch(
            update_todo_status_url(res_init_card.data['id']),
            payload_not_done)
        self.assertEqual(
            res_set_status_not_done.status_code,
            status.HTTP_200_OK)
        todo_card.refresh_from_db()
        self.assertEqual(todo_card.done_at, None)
        self.assertEqual(
            res_set_status_not_done.data['done_at'],
            None)
        for key, value in res_set_status_not_done.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_card, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(getattr(todo_card, key), value)

    def test_get_todo_card_detail(self):
        # test get method success
        todo_create = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)

        todo_id = todo_create.data['id']
        todo_get = self.client.get(todo_card_detail_url(todo_id))
        self.assertEqual(
            todo_get.status_code,
            status.HTTP_200_OK)

        # check res & database is the same data
        todo = TodoCard.objects.get(pk=todo_id)
        for key, value in todo_get.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo, key),
                    value)

    def test_delete_todo_card(self):
        # test delete method
        res_create_todo = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        todo_id = res_create_todo.data['id']
        res_del = self.client.delete(todo_card_detail_url(todo_id))
        self.assertEqual(
            res_del.status_code,
            status.HTTP_204_NO_CONTENT)

        # test resource not found after delete
        res_get_todo_deleted = self.client.get(todo_card_detail_url(todo_id))
        self.assertEqual(
            res_get_todo_deleted.status_code,
            status.HTTP_404_NOT_FOUND)

    def test_pick_color_todo_card(self):
        # test patch method to update color of each colors
        res_create_todo = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        color_list = ['HT', 'H', 'L', 'LT']
        for cl in color_list:
            # test method
            payload_update_color = {'color': cl}
            todo_id = res_create_todo.data['id']
            res_pick_color = self.client.patch(
                todo_card_detail_url(todo_id),
                payload_update_color)
            self.assertEqual(
                res_pick_color.status_code,
                status.HTTP_200_OK)
            self.assertEqual(res_pick_color.data['color'], cl)

            # check res & database is the same data
            todo = TodoCard.objects.get(pk=todo_id)
            for key, value in res_pick_color.data.items():
                if value and key in timezone_field:
                    self.assertEqual(
                        getattr(todo, key),
                        datetime.datetime.fromisoformat(value))
                else:
                    self.assertEqual(getattr(todo, key), value)
