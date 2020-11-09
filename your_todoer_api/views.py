from django.contrib.auth.models import User
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from your_todoer_api.models import Project, Task
from your_todoer_api.serializers import (UserSerializer,
                                         ProjectSerializer,
                                         TaskSerializer)
from your_todoer_api.permissions import IsAnonymous, IsOwner


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(pk=current_user.pk)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAnonymous]


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(pk=current_user.pk)


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return Project.objects.filter(owner=current_user)


class ProjectCreateAPIView(CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        current_user = self.request.user
        return Project.objects.filter(owner=current_user)


class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        user_projects = Project.objects.filter(owner=current_user)
        current_project = user_projects.get(pk=self.kwargs['project_pk'])
        tasks = current_project.tasks
        return tasks


class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        current_user = self.request.user
        user_projects = Project.objects.filter(owner=current_user)
        current_project = user_projects.get(pk=self.kwargs['project_pk'])
        serializer.save(owner=current_user, project=current_project)


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        current_user = self.request.user
        user_projects = Project.objects.filter(owner=current_user)
        current_project = user_projects.get(pk=self.kwargs['project_pk'])
        tasks = current_project.tasks
        return tasks
