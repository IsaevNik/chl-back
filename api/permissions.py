from rest_framework import permissions

from api.models.support import Support


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Support.get_support_by_user(request.user).is_admin


class IsSupport(permissions.BasePermission):
    def has_permisson(self, request, view):
        try:
            Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return Support.get_support_by_user(request.user).is_admin


class IsAdminOrGroupSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        support = Support.get_support_by_user(request.user)
        if (request.method in permissions.SAFE_METHODS and 
            obj.support == support) or support.is_admin:
            return True
