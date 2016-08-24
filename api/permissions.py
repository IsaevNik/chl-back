from rest_framework import permissions

from api.models.support import Support


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Support.get_support_by_user(request.user).is_admin
