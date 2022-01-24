from rest_framework.permissions import BasePermission


class IsAdminOrIsSelf(BasePermission):
    """
    Object-level permission to only allow user to edit only their data.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (obj == request.user)
