from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUnAuthenticated(BasePermission):
    message = 'User is already logged-in.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow author to edit only their posts.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsUserThemselves(BasePermission):
    """
    Object-level permission to only allow user to edit only their data.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
