from django.contrib.auth.models import User
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from your_todoer_api.models import Project, Task
from your_todoer_api.serializers import (UserSerializer,
                                         ProjectSerializer,
                                         TaskSerializer)
from your_todoer_api.permissions import IsAnonymous


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
