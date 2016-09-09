from rest_framework import permissions

from api.models.support import Support


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Support.get_support_by_user(request.user).is_admin



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return Support.get_support_by_user(request.user).is_admin


class IsAdminOrBooker(permissions.BasePermission):
    def has_permission(self, request, view):
        support = Support.get_support_by_user(request.user)
        if request.method in permissions.SAFE_METHODS and support.is_superadmin:
            return True
        if support.is_admin or support.is_booker:
            return True
        else:
            return False


class IsAdminOrGroupSupportAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        support = Support.get_support_by_user(request.user)
        if (request.method in permissions.SAFE_METHODS and 
            obj.support == support) or support.is_admin:
            return True
        else:
            return False


class IsAdminOrGroupSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        support = Support.get_support_by_user(request.user)
        if obj.support == support or support.is_admin:
            return True
        else:
            return False


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return Support.get_support_by_user(request.user).is_superadmin


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if (Support.get_support_by_user(request.user).is_admin or 
            Support.get_support_by_user(request.user).is_superadmin):
            return True
        else:
            return False


class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        if support.is_booker:
            return False
        return True