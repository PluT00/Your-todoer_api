"""your_todoer_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from your_todoer_api.views import (UserListAPIView, UserCreateAPIView,
                                   UserDetailAPIView, ProjectListAPIView,
                                   ProjectCreateAPIView, ProjectDetailAPIView,
                                   TaskListAPIView, TaskCreateAPIView,
                                   TaskDetailAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserListAPIView.as_view()),
    path('api/user/create/', UserCreateAPIView.as_view()),
    path('api/user/<int:pk>/', UserDetailAPIView.as_view()),
    path('api/projects/', ProjectListAPIView.as_view()),
    path('api/projects/create/', ProjectCreateAPIView.as_view()),
    path('api/projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('api/projects/<int:project_pk>/tasks/', TaskListAPIView.as_view()),
    path('api/projects/<int:project_pk>/tasks/create/',
         TaskCreateAPIView.as_view()),
    path('api/projects/<int:project_pk>/tasks/<int:pk>/',
         TaskDetailAPIView.as_view()),
]
