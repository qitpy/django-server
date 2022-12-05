from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app_todo import serializers

from core.models import (
    TodoCard,
    UserTodo,
)

import datetime
import random


TODO_CARD_URL = reverse('app_todo:todo_card-list')
TODO_CARD_BY_COLOR_URL = \
    reverse('app_todo:todo_card-sort-by-color')


def list_and_filtering_todo_card_sort_by_color_url(**kwargs):
    url = reverse('app_todo:todo_card-sort-by-color')
    is_done = kwargs['is_done']
    return f'{url}?is_done={is_done}'


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
        self.factory = RequestFactory()

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
        res = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        todo_card_id = res.data['id']
        res_patch = self.client.patch(
          todo_card_detail_url(pk=todo_card_id),
          payload_update
        )
        self.assertEqual(
            res_patch.status_code,
            status.HTTP_200_OK)
        self.assertEqual(res_patch.data['done_at'], None)
        todo_card_updated = TodoCard.objects.get(pk=todo_card_id)

        # check payload with database is the same data
        for key, value, in payload_update.items():
            self.assertEqual(
                getattr(todo_card_updated, key),
                value)

        # test response with database valid
        for key, value in res_patch.data.items():
            if value and key in timezone_field:
                self.assertEqual(
                    getattr(todo_card_updated, key),
                    datetime.datetime.fromisoformat(value))
            else:
                self.assertEqual(
                    getattr(todo_card_updated, key),
                    value)

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

    def test_list_todo_card(self):
        # create todo for default user
        res_todo_1 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        res_todo_2 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        res_todo_3 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)

        # create other user and todo of that user
        other_user = create_user(email='other@user.com')
        other_user_todo = UserTodo.objects.create(user=other_user)
        TodoCard.objects.create(
            user_todo=other_user_todo,
            **payload_create_todo_card_default)
        TodoCard.objects.create(
            user_todo=other_user_todo,
            **payload_create_todo_card_default)

        # test list method
        res_list_todo = self.client.get(TODO_CARD_URL)
        self.assertEqual(
            res_list_todo.status_code,
            status.HTTP_200_OK)
        todo_id_arr = [
            res_todo_1.data['id'],
            res_todo_2.data['id'],
            res_todo_3.data['id']]
        for res_data in res_list_todo.data:
            item_id = res_data['id']
            self.assertTrue(item_id in todo_id_arr)
            todo_card_item = TodoCard.objects.get(pk=item_id)
            self.assertEqual(
                res_data,
                serializers.TodoCardSerializer(todo_card_item).data)
            todo_id_arr.remove(item_id)
        self.assertFalse(todo_id_arr)

    def test_list_todo_card_ordering_by_time(self):
        """test that GET list return that ordered by update time"""
        res_todo_1 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        res_todo_2 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)
        res_todo_3 = self.client.post(
            TODO_CARD_URL,
            payload_create_todo_card_default)

        res_expect = [
            res_todo_1.data['id'],
            res_todo_2.data['id'],
            res_todo_3.data['id']]

        res_list_todo = self.client.get(TODO_CARD_URL)
        for i, x in enumerate(res_list_todo.data):
            self.assertEqual(x['id'], res_expect[i])

    # def test_get_list_todo_card_sort_by_color(self):
    #     # initial list todo_task
    #     color_list = [
    #         TodoCard.TodoCardColor.PINK,
    #         TodoCard.TodoCardColor.ORANGE,
    #         TodoCard.TodoCardColor.BLUE,
    #         TodoCard.TodoCardColor.GREEN]
    #     payload = {
    #         'name': 'test_todo',
    #         'description': 'this is task for testing'
    #     }
    #     res_list = []
    #     for x in range(10):
    #         payload['color'] = random.choice(color_list)
    #         res = self.client.post(
    #             TODO_CARD_URL,
    #             payload)
    #         res_list.append(res.data)

    #     # expect response design
    #     pink_task = filter(
    #         lambda x: x['color'] == TodoCard.TodoCardColor.PINK,
    #         res_list)
    #     orange_task = filter(
    #         lambda x: x['color'] == TodoCard.TodoCardColor.ORANGE,
    #         res_list)
    #     blue_task = filter(
    #         lambda x: x['color'] == TodoCard.TodoCardColor.BLUE,
    #         res_list)
    #     green_task = filter(
    #         lambda x: x['color'] == TodoCard.TodoCardColor.GREEN,
    #         res_list)

    #     pink_task_expect = \
    #         [serializers.TodoCardSerializer(x).data for x in pink_task]
    #     orange_task_expect = \
    #         [serializers.TodoCardSerializer(x).data for x in orange_task]
    #     blue_task_expect = \
    #         [serializers.TodoCardSerializer(x).data for x in blue_task]
    #     green_task_expect = \
    #         [serializers.TodoCardSerializer(x).data for x in green_task]

    #     # assert as design response
    #     res = self.client.get(TODO_CARD_BY_COLOR_URL)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(pink_task_expect, res.data['pink_task'])
    #     self.assertEqual(orange_task_expect, res.data['orange_task'])
    #     self.assertEqual(blue_task_expect, res.data['blue_task'])
    #     self.assertEqual(green_task_expect, res.data['green_task'])

    def test_filter_task_by_done_status(self):
        # initial list todo_task
        color_list = [
            TodoCard.TodoCardColor.PINK,
            TodoCard.TodoCardColor.ORANGE,
            TodoCard.TodoCardColor.BLUE,
            TodoCard.TodoCardColor.GREEN]
        payload = {
            'name': 'test_todo',
            'description': 'this is task for testing'
        }
        res_list = []
        for _ in range(10):
            payload['color'] = random.choice(color_list)
            res = self.client.post(
                TODO_CARD_URL, payload)
            payload_done_status = \
                {'is_done': random.choice([True, False])}
            res_set_done = self.client.patch(
                update_todo_status_url(res.data['id']),
                payload_done_status)
            res_list.append(res_set_done.data)

        # make request to test
        query_params_done_task = {
            'is_done': True
        }
        query_params_not_done_task = {
            'is_done': False
        }
        res_done_task = self.client.get(
            list_and_filtering_todo_card_sort_by_color_url(
                **query_params_done_task))
        res_not_done_task = self.client.get(
            list_and_filtering_todo_card_sort_by_color_url(
                **query_params_not_done_task))

        expect_item_done_task = list(filter(
                lambda x: x['done_at'] is not None, res_list))
        expect_item_not_done_task = list(filter(
                lambda x: x['done_at'] is None, res_list))

        for key, _ in res_done_task.data.items():
            for task_done in res_done_task.data[key]:
                self.assertIn(dict(task_done), expect_item_done_task)
        for key, _ in res_not_done_task.data.items():
            for task_not_done in res_not_done_task.data[key]:
                self.assertIn(dict(task_not_done), expect_item_not_done_task)
