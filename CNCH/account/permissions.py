from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Allow access only to admins (role == 'admin' or superuser/staff)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.role == 'admin'))
