from django.contrib.auth.models import User
from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework import serializers

from your_todoer_api.models import Task
from your_todoer_api.serializers import UserSerializer, TaskSerializer


class TaskSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.task_attributes = {'title': "Test",
                                'is_completed': False,
                                'owner': self.user}
        self.task = Task.objects.create(**self.task_attributes)
        self.serializer = TaskSerializer(instance=self.task)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                             set(['id', 'title', 'is_completed', 'owner']))

    def test_title_field(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.task_attributes['title'])

    def test_is_completed_field(self):
        data = self.serializer.data
        self.assertEqual(
            data['is_completed'], self.task_attributes['is_completed'])

    def test_uesr_field(self):
        data = self.serializer.data
        self.assertEqual(data['owner'], self.user.id)


class UserSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {'username': "test",
                                'email': "test@email.com",
                                'password': "test"}
        self.serializer_user_attributes = {'username': "test2",
                                                   'email': "test2@email.com",
                                                   'password': "test2"}
        self.user = User.objects.create_user(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                         set(['id', 'username', 'tasks', 'email']))

    def test_username_field(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])

    def test_email_field(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_password_field(self):
        password = self.serializer.get_fields()['password']
        write_only = password.write_only
        required = password.required
        allow_blank = password.allow_blank

        self.assertEqual(write_only, True)
        self.assertEqual(required, True)
        self.assertEqual(allow_blank, False)

    def test_tasks_field(self):
        read_only = self.serializer.get_fields()['tasks'].read_only
        self.assertEqual(read_only, True)

    def test_create_method(self):
        new_user = UserSerializer().create(self.serializer_user_attributes)
        logged_in = self.client.login(
            username=self.serializer_user_attributes['username'],
            password=self.serializer_user_attributes['password'])

        self.assertEqual(new_user.username,
                         self.serializer_user_attributes["username"])
        self.assertEqual(new_user.email,
                         self.serializer_user_attributes["email"])
        self.assertEqual(new_user.has_usable_password(), True)
        self.assertEqual(logged_in, True)

    def test_update_method(self):
        new_attributes = {
            'username': 'newusername',
            'email': 'new@email.com',
            'password': 'NewPassword1'
        }
        new_user = UserSerializer().create(self.serializer_user_attributes)
        updated_user = UserSerializer().update(new_user, new_attributes)
        logged_in = self.client.login(
            username=new_attributes['username'],
            password=new_attributes['password']
        )

        self.assertEqual(updated_user.username, new_attributes['username'])
        self.assertEqual(updated_user.email, new_attributes['email'])
        self.assertEqual(updated_user.has_usable_password(), True)
        self.assertEqual(logged_in, True)

    def test_validation_with_not_unique_username(self):
        new_data = self.serializer_user_attributes

        new_data['username'] = self.user_attributes['username']
        new_serializer_usename_lower = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_usename_lower.is_valid(), False)

        new_data['username'] = self.user_attributes['username'].capitalize()
        new_serializer_usename_capitalize = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_usename_capitalize.is_valid(), False)

        new_data['username'] = self.user_attributes['username'].upper()
        new_serializer_usename_upper = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_usename_upper.is_valid(), False)

    def test_validation_without_username(self):
        new_data = self.serializer_user_attributes
        new_data.pop('username')
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_blank_username(self):
        new_data = self.serializer_user_attributes
        new_data['username'] = ''
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_not_unique_email(self):
        new_data = self.serializer_user_attributes

        new_data['email'] = self.user_attributes['email']
        new_serializer_lower = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_lower.is_valid(), False)

        new_data['email'] = self.user_attributes['email'].capitalize()
        new_serializer_capitalize = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_capitalize.is_valid(), False)

        new_data['email'] = self.user_attributes['email'].upper()
        new_serializer_upper = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_upper.is_valid(), False)

    def test_validation_without_email(self):
        new_data = self.serializer_user_attributes
        new_data.pop('email')
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_blank_email(self):
        new_data = self.serializer_user_attributes
        new_data['email'] = ''
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_invalid_email(self):
        new_data = self.serializer_user_attributes
        new_data['email'] = 'test'
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_valid_password(self):
        new_data = self.serializer_user_attributes
        new_data['password'] = 'Testpassword1'
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), True)

    def test_validation_without_password(self):
        new_data = self.serializer_user_attributes
        new_data.pop('password')
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_blank_password(self):
        new_data = self.serializer_user_attributes
        new_data['password'] = ''
        new_serializer = UserSerializer(data=new_data)
        self.assertEqual(new_serializer.is_valid(), False)

    def test_validation_with_invalid_password(self):
        new_data = self.serializer_user_attributes

        new_data['password'] = '1Abc'
        new_serializer_with_short_passwd = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_with_short_passwd.is_valid(), False)

        new_data['password'] = 'AbcdEfghi'
        new_serializer_passwd_without_digit = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_passwd_without_digit.is_valid(), False)

        new_data['password'] = '1abcdefgh'
        new_serializer_passwd_without_capital = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_passwd_without_capital.is_valid(),
                         False)

        new_data['password'] = '1ABCDEFGH'
        new_serializer_passwd_without_lowecase = UserSerializer(data=new_data)
        self.assertEqual(new_serializer_passwd_without_lowecase.is_valid(),
                         False)
