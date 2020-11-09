from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory, TestCase

from your_todoer_api.permissions import IsAnonymous, IsOwner
from your_todoer_api.models import Project


class IsAnonymousTestCase(TestCase):

    def setUp(self):
        self.anonymous_user = AnonymousUser()
        self.user = User.objects.create(username='test')
        self.factory = RequestFactory()
        self.permission_check = IsAnonymous()

    def test_anonymous_user(self):
        request = self.factory.get('/')
        request.user = self.anonymous_user
        permission = self.permission_check.has_permission(request, None)

        self.assertEqual(permission, True)

    def test_not_anonymous_user(self):
        request = self.factory.get('/')
        request.user = self.user
        permission = self.permission_check.has_permission(request, None)

        self.assertEqual(permission, False)


class IsOwnerTestCase(TestCase):

    def setUp(self):
        self.owner_user = User.objects.create(username='test')
        self.not_owner_user = User.objects.create(username='test2')
        self.project = Project.objects.create(name='test_project',
                                              owner=self.owner_user)
        self.factory = RequestFactory()
        self.permission_check = IsOwner()

    def test_owner_user(self):
        request = self.factory.get('/')
        request.user = self.owner_user
        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.project
        )

        self.assertEqual(permission, True)

    def test_not_owner_user(self):
        request = self.factory.get('/')
        request.user = self.not_owner_user
        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.project
        )

        self.assertEqual(permission, False)
