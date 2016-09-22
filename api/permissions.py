from rest_framework import permissions
from django.utils import timezone

from api.models.support import Support
from api.models.agent import Agent
from api.utils.exceptions.company import SubcriptionTimeOutException

# checked
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            if support.is_operator and (request.method in permissions.SAFE_METHODS):
                return True
            return support.is_admin
        except Support.DoesNotExist:
            return False

# checked
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            return support.is_admin
        except Support.DoesNotExist:
            return False

#checked
class IsCompanyActiveOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            if request.method in permissions.SAFE_METHODS:
                return True
            if support.company.time_to_finish_subscription < timezone.now():
                raise SubcriptionTimeOutException()
            else:
                return True
        except Support.DoesNotExist:
            return False

#checked
class IsCompanyActive(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            if support.company.time_to_finish_subscription < timezone.now():
                raise SubcriptionTimeOutException()
            else:
                return True
        except Support.DoesNotExist:
            return False


class IsAdminOrBooker(permissions.BasePermission):
    def has_permission(self, request, view):
        support = Support.get_support_by_user(request.user)
        if request.method in permissions.SAFE_METHODS and support.is_superadmin:
            return True
        if support.is_admin or support.is_booker:
            return True
        else:
            return False

#checked
class IsThisCompanyObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            support = Support.get_support_by_user(request.user)
            if support.is_superadmin and (request.method in permissions.SAFE_METHODS):
                return True
            return support.company == obj.company
        except Support.DoesNotExist:
            return False


class IsAdminOrGroupSupportAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        company = obj.support.company
        try:
            support = Support.get_support_by_user(request.user)
            return (request.method in permissions.SAFE_METHODS and obj.support == support) or \
                (support.is_admin and support.company == company)
        except Support.DoesNotExist:
            return False


class IsAdminOrGroupSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        support = Support.get_support_by_user(request.user)
        if (obj.support == support or 
            support.company == obj.support.company and support.is_admin):
            return True
        else:
            return False

#checked
class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            return support.is_superadmin
        except Support.DoesNotExist:
            return False


#checked
class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            return (support.is_admin or support.is_superadmin)
        except Support.DoesNotExist:
            return False

#checked
class IsSupportInstance(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        return True


class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        if support.is_booker:
            return False
        return True


class IsThisGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        agent = Agent.get_agent_by_user(request.user)
        if not obj:
            return True
        if agent.group == obj:
            return True
        else:
            return False


class IsThisTaskExecuter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        agent = Agent.get_agent_by_user(request.user)
        if obj.executer == agent:
            return True
        else:
            return False

class IsAdminOrAgentOfYourGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False

        group = obj.group
        if group.support == support or support.is_admin:
            return True
        else:
            return False


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            agent = Agent.get_agent_by_user(request.user)
        except Agent.DoesNotExist:
            return False
        return True


class IsThisPayAgent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        agent = Agent.get_agent_by_user(request.user)
        if obj.agent == agent:
            return True
        else:
            return False