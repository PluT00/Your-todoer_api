import re
from django.contrib.auth.models import User
from rest_framework import serializers

from your_todoer_api.models import Task, Project


def validate_username(value):
    """
    Check `User` instance for unique `username`.
    """
    check_query = User.objects.filter(username__iexact=value)
    if len(check_query) > 0:
        raise serializers.ValidationError('A user with this name already exists.')
    return value


def validate_email(value):
    """
    Check `User` instance for unique `email`.
    """
    check_query = User.objects.filter(email__iexact=value)
    if len(check_query) > 0:
        raise serializers.ValidationError('A user with this email already exists.')
    return value

def validate_password(value):
    """
    Check `User` instance for valid `password`.

    Must be at least 8 characters long, have one capital letter,
    one lowercase letter and one digit.
    """
    validation_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9]{8,64}$"
    if not re.match(validation_pattern, value):
        raise serializers.ValidationError("Password must be at least 8 "
                                          "characters long, have one capital, "
                                          "one lowercase letters and one digit.")
    return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'project', 'owner']
        read_only_fields = ['project', 'owner']


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks', 'owner']
        read_only_fields = ['owner']


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    email = serializers.EmailField(validators=[validate_email])

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return `User` instance,
        given the instance and the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'projects', 'tasks', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                     'validators': [validate_password],
                                     'style': {'input_type': 'password'}},
                        'username': {'validators': [validate_username]}}
