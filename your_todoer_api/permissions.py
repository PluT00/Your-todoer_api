from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """
    Permission to only allow anonymous users create new users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        return False
