from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """
    Permission to only allow anonymous users create new users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to have an
    access to it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
