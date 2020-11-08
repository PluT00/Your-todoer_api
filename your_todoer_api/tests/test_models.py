from django.contrib.auth.models import User
from django.test import TestCase

from your_todoer_api.models import Task, Project


class TaskModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.project = Project.objects.create(
            name="test_project",
            owner=self.user
        )
        self.task = Task.objects.create(
            title="test_task",
            project=self.project,
            owner=self.user
        )

    def test_title_field(self):
        max_length = self.task._meta.get_field('title').max_length
        self.assertEqual(max_length, 1500)

    def test_owner_field(self):
        related_model = self.task._meta.get_field('owner').related_model
        self.assertEqual(related_model, User)

    def test_project_field(self):
        related_model = self.task._meta.get_field('project').related_model
        self.assertEqual(related_model, Project)

    def test__str__method(self):
        self.assertEqual(
            self.task.__str__(),
            f'{self.task.owner.username} | {self.task.project.name}:{self.task.title}'
        )


class ProjectModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.project = Project.objects.create(
            name="test_project", owner=self.user
        )

    def test_name_field(self):
        max_length = self.project._meta.get_field('name').max_length
        self.assertEqual(max_length, 500)

    def test_owner_field(self):
        related_model = self.project._meta.get_field('owner').related_model
        self.assertEqual(related_model, User)

    def test__str__method(self):
        self.assertEqual(
            self.project.__str__(),
            f'{self.project.owner.username} | {self.project.name}'
        )
