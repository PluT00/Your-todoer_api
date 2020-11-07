from django.contrib.auth.models import User
from django.test import TestCase

from todoapp_api.models import Task


class TaskModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.task = Task.objects.create(
            title="test_task", is_completed=False, user=self.user
            )

    def test_title_field(self):
        max_length = self.task._meta.get_field('title').max_length
        self.assertEqual(max_length, 1500)

    def test_is_completed_field(self):
        default = self.task._meta.get_field('is_completed').default
        self.assertEqual(default, False)

    def test_user_field(self):
        related_model = self.task._meta.get_field('user').related_model
        self.assertEqual(related_model, User)

    def test__str__method(self):
        self.assertEqual(
            self.task.__str__(),
            f'{self.task.id} | {self.task.title}'
            )
