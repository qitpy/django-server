from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app_todo import serializers

from core.models import (
    TodoDaily,
    UserTodo,
)

import datetime
import random


TODO_DAILY_URL = reverse('app_todo:todo_daily-list')


def todo_daily_detail_url(pk):
    return reverse('app_todo:todo_daily-detail', args=[pk])

def update_todo_daily_done_status_url(pk):
    return reverse('app_todo:todo_daily-set-done', args=[pk])

def create_user(email='quyet.doan@gmail.com', name='User-name'):
    return get_user_model().objects.create_user(email, name)


payload_create_todo_daily_default = {
    'name': 'todo task name test',
    'description': 'descriptions of the task test',
}

timezone_field = ['updated_at', 'created_at', 'done_at']


class PublicTodoDailyApiTest(TestCase):
    """test unauthenticated API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TODO_DAILY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoDailyApiTest(TestCase):
    """test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)


    def test_todo_daily_create_successful(self):
        res = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(res.data['done_at'])
        self.assertIsNotNone(res.data['created_at'])
        self.assertIsNotNone(res.data['updated_at'])

        # validate response compatible with database
        todo_daily_id = res.data['id']
        todo_daily = TodoDaily.objects.get(pk=todo_daily_id)
        for key, value in payload_create_todo_daily_default.items():
            self.assertEqual(res.data[key], value)
        self.assertTrue(todo_daily.user_todo.user_id == self.user.id)

        # test response with database valid
        for key, value in res.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_daily, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(getattr(todo_daily, key), value)

    def test_todo_daily_create_api_failed(self):
        """test create case failed when create todo_daily"""
        # value is not blank at field 'name'
        payload = {
            'name': '',
            'description': ''
        }
        res = self.client.post(TODO_DAILY_URL, payload)
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST)

        # 'name' is required
        payload = {
            'description': 'test description'
        }
        payload_empty = {}
        self.client.post(TODO_DAILY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.post(TODO_DAILY_URL, payload_empty)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_todo_daily_successful(self):
        """test update todo_daily that will be success"""
        # create todo_daily
        payload_update = {
            'name': 'this is the task updated',
            'description': 'this is my the updating of the description'
        }
        res = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        todo_daily_id = res.data['id']
        res_patch = self.client.patch(
          todo_daily_detail_url(pk=todo_daily_id),
          payload_update
        )
        self.assertEqual(
            res_patch.status_code,
            status.HTTP_200_OK)
        self.assertEqual(res_patch.data['done_at'], None)
        todo_daily_updated = TodoDaily.objects.get(pk=todo_daily_id)

        # check payload with database is the same data
        for key, value, in payload_update.items():
            self.assertEqual(
                getattr(todo_daily_updated, key),
                value)

        # test response with database valid
        for key, value in res_patch.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_daily_updated, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo_daily_updated, key),
                    value)

    def test_set_todo_daily_status(self):
        payload_done = {
            'is_done': True
        }
        payload_not_done = {
            'is_done': False
        }
        res_init_card = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        todo_daily = TodoDaily.objects.get(pk=res_init_card.data['id'])

        # test done task
        res_set_status_done = self.client.patch(
            update_todo_daily_done_status_url(res_init_card.data['id']),
            payload_done)
        todo_daily.refresh_from_db()
        self.assertEqual(
            res_set_status_done.status_code,
            status.HTTP_200_OK)
        self.assertNotEqual(
            todo_daily.done_at,
            None)
        self.assertNotEqual(
            res_set_status_done.data['done_at'],
            None)
        for key, value in res_set_status_done.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_daily, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo_daily, key),
                    value)

        # test not done task
        res_set_status_not_done = self.client.patch(
            update_todo_daily_done_status_url(res_init_card.data['id']),
            payload_not_done)
        self.assertEqual(
            res_set_status_not_done.status_code,
            status.HTTP_200_OK)
        todo_daily.refresh_from_db()
        self.assertEqual(todo_daily.done_at, None)
        self.assertEqual(
            res_set_status_not_done.data['done_at'],
            None)
        for key, value in res_set_status_not_done.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_daily, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(getattr(todo_daily, key), value)

    def test_get_todo_daily_detail(self):
        # test get method success
        todo_create = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)

        todo_id = todo_create.data['id']
        todo_get = self.client.get(todo_daily_detail_url(todo_id))
        self.assertEqual(
            todo_get.status_code,
            status.HTTP_200_OK)

        # check res & database is the same data
        todo = TodoDaily.objects.get(pk=todo_id)
        for key, value in todo_get.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo, key),
                    value)

    def test_delete_todo_daily(self):
        # test delete method
        res_create_todo = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        todo_id = res_create_todo.data['id']
        res_del = self.client.delete(todo_daily_detail_url(todo_id))
        self.assertEqual(
            res_del.status_code,
            status.HTTP_204_NO_CONTENT)

        # test resource not found after delete
        res_get_todo_deleted = self.client.get(todo_daily_detail_url(todo_id))
        self.assertEqual(
            res_get_todo_deleted.status_code,
            status.HTTP_404_NOT_FOUND)

    def test_list_todo_daily(self):
        # create todo for default user
        res_list_created = []
        for _ in range(10):
            res = self.client.post(
                TODO_DAILY_URL,
                payload_create_todo_daily_default)
            res_list_created.append(res.data)


        # create other user and todo of that user
        other_user = create_user(email='other@user.com')
        other_user_todo = UserTodo.objects.create(user=other_user)
        TodoDaily.objects.create(
            user_todo=other_user_todo,
            **payload_create_todo_daily_default)
        TodoDaily.objects.create(
            user_todo=other_user_todo,
            **payload_create_todo_daily_default)

        # test list method
        res_list_todo = self.client.get(TODO_DAILY_URL)
        self.assertEqual(
            res_list_todo.status_code,
            status.HTTP_200_OK)
        todo_id_arr = list(map(lambda x: x['id'], res_list_created))
        for res_data in res_list_todo.data:
            item_id = res_data['id']
            self.assertTrue(item_id in todo_id_arr)
            todo_daily_item = TodoDaily.objects.get(pk=item_id)
            self.assertEqual(
                dict(res_data),
                serializers.DailySerializer(todo_daily_item).data)
            todo_id_arr.remove(item_id)
        self.assertFalse(todo_id_arr)

    def test_list_todo_daily_ordering_by_time(self):
        """test that GET list return that ordered by update time"""
        res_todo_1 = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        res_todo_2 = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)
        res_todo_3 = self.client.post(
            TODO_DAILY_URL,
            payload_create_todo_daily_default)

        res_expect = [
            res_todo_1.data['id'],
            res_todo_2.data['id'],
            res_todo_3.data['id']]

        res_list_todo = self.client.get(TODO_DAILY_URL)
        for i, x in enumerate(res_list_todo.data):
            self.assertEqual(x['id'], res_expect[i])

