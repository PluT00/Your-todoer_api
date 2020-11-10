import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.renderers import JSONRenderer

from your_todoer_api.models import Project, Task
from your_todoer_api.serializers import (UserSerializer, ProjectSerializer,
                                         TaskSerializer)


class UserViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_credentials = {
            'username': "test",
            'password': "test"
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)
        not_listed_user = User.objects.create(username="not_listed")
        self.new_user_data = {
            'username': 'test2',
            'email': 'test@email.com',
            'password': 'NewTestPass1'
        }

    def test_user_get_view(self):
        response = self.client.get(reverse('user_get_url'))
        serializer = UserSerializer(self.user)
        response_content = JSONRenderer().render([serializer.data])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_content)

    def test_user_get_view_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('user_get_url'))

        self.assertEqual(response.status_code, 403)

    def test_user_create_view(self):
        self.client.logout()
        response = self.client.post(reverse('user_create_url'),
                                    self.new_user_data, format='json')
        user = User.objects.get(username=self.new_user_data['username'])
        serializer = UserSerializer(user)
        response_content = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, response_content)

    def test_user_create_view_not_anonymous(self):
        response = self.client.post(reverse('user_create_url'),
                                    self.new_user_data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_user_retrieve_view(self):
        response = self.client.get(reverse('user_retrieve_url',
                                           kwargs={'pk': self.user.id}))
        serializer = UserSerializer(self.user)
        response_content = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_content)

    def test_user_retrieve_view_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('user_retrieve_url',
                                           kwargs={'pk': self.user.id}))

        self.assertEqual(response.status_code, 403)


class ProjectViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_credentials = {
            'username': "test",
            'password': "test"
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)
        self.project = Project.objects.create(name="test_proj", owner=self.user)
        not_used_user = User.objects.create(username="not_used")
        not_listed_project = Project.objects.create(name="not_listed",
                                  owner=not_used_user)
        self.new_project_data = {
            'name': "test2",
            'owner': self.user.id
        }

    def test_project_list_view(self):
        response = self.client.get(reverse('projects_list_url'))

        serializer = ProjectSerializer(self.project)
        response_content = JSONRenderer().render([serializer.data])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_content)

    def test_project_list_view_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('projects_list_url'))

        self.assertEqual(response.status_code, 403)

    def test_project_create_view(self):
        response = self.client.post(reverse('project_create_url'),
                                    self.new_project_data, format='json')

        project = Project.objects.get(name=self.new_project_data['name'])
        serializer = ProjectSerializer(project)
        response_content = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, response_content)

    def test_project_create_view_anonymous(self):
        self.client.logout()
        response = self.client.post(reverse('project_create_url'),
                                    self.new_project_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_project_details_view(self):
        response = self.client.get(reverse('project_details_url',
                                           kwargs={'pk': self.project.id}))

        serializer = ProjectSerializer(self.project)
        response_content = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_content)

    def test_project_details_view_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('project_details_url',
                                           kwargs={'pk': self.project.id}))

        self.assertEqual(response.status_code, 403)


class TaskViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_credentials = {
            'username': "test",
            'password': "test"
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)
        self.project = Project.objects.create(name="test_proj", owner=self.user)
        self.task = Task.objects.create(title="test_task", project=self.project,
                                        owner=self.user)
        not_used_user = User.objects.create(username="not_used")
        not_listed_project = Project.objects.create(
            name="not_listed",
            owner=not_used_user
        )
        not_listed_task = Task.objects.create(title="not_listed",
                                              project=not_listed_project,
                                              owner=not_used_user)
        self.new_task_data = {
            'titel': 'test2',
            'project': self.project.id,
            'owner': self.user.id
        }

        def test_task_list_view(self):
            response = self.client.get(reverse(
                'tasks_list_url',
                kwargs={'project_pk': self.project.id}
            ))
            serailizer = TaskSerializer(self.task)
            response_content = JSONRenderer().render([serializer.data])

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, response_content)

        def test_task_list_view_anonymous(self):
            self.client.logout()
            response = self.client.get(reverse(
                'tasks_list_url',
                kwargs={'project_pk': self.project.id}
            ))

            self.assertEqual(response.status_code, 403)

        def test_task_create_view(self):
            response = self.client.post(
                reverse(
                    'tasks_list_url',
                    kwargs={'project_pk': self.project.id}
                ),
                self.new_task_data
            )
            task = Task.objects.get(title=self.new_task_data['titel'])
            serializer = TaskSerializer(task)
            response_content = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content, response_content)

        def test_task_create_view_anonymous(self):
            self.client.logout()
            response = self.client.post(
                reverse(
                    'tasks_list_url',
                    kwargs={'project_pk': self.project.id}
                ),
                self.new_task_data
            )

            self.assertEqual(response.status_code, 403)

        def test_task_details_view(self):
            response = self.client.get(reverse(
                'task_details_url',
                kwargs={'project_pk': self.project.id, 'pk': self.task.id}
            ))
            task = Task.objects.get(pk=self.task.id)
            serializer = TaskSerializer(task)
            response_content = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, response_content)

        def test_task_details_view_anonymous(self):
            self.client.logout()
            response = self.client.get(reverse(
                'task_details_url',
                kwargs={'project_pk': self.project.id, 'pk': self.task.id}
            ))

            self.assertEqual(response.status_code, 403)
