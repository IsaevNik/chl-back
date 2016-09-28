# coding=utf-8
from rest_framework import permissions
from django.utils import timezone

from api.models.support import Support
from api.models.agent import Agent
from api.models.subscription import Subscription
from api.utils.exceptions.subscription import SubcriptionTimeOutException
from api.service.task import get_start_task_by_company

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

#checked
class IsAdminOrBooker(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False

        return (request.method in permissions.SAFE_METHODS and support.is_superadmin) or \
               (support.is_admin or support.is_booker)

#checked
class IsAdminReadOnlyOrBooker(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False

        return (request.method in permissions.SAFE_METHODS and support.is_superadmin) or \
               (request.method in permissions.SAFE_METHODS and support.is_admin) \
               or support.is_booker

#checked
class IsThisCompanyObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            support = Support.get_support_by_user(request.user)
            # бухгалтер имеет доступ к подпискам компании
            if isinstance(obj, Subscription) and support.is_booker:
                return True
            if support.is_superadmin and (request.method in permissions.SAFE_METHODS):
                return True
            return support.company == obj.company
        except Support.DoesNotExist:
            return False

#checked
class IsAdminOrGroupSupportAndReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, group):
        company = group.support.company
        try:
            support = Support.get_support_by_user(request.user)
            return (request.method in permissions.SAFE_METHODS and group.support == support) or \
                (support.is_admin and support.company == company)
        except Support.DoesNotExist:
            return False

#checked
class IsAdminOrGroupSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, group):
        try:
            support = Support.get_support_by_user(request.user)
            return (group.support == support or 
            support.company == group.support.company and support.is_admin)
        except Support.DoesNotExist:
            return False

#checked
class IsSupportTask(permissions.BasePermission):
    def has_object_permission(self, request, view, task):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        group = task.group
        if not group:
            start_task = get_start_task_by_company(support.company)
            if task != start_task:
                return False
            elif not support.is_admin and not request.method in permissions.SAFE_METHODS:
                return False
            else:
                return True
        else: 
            return (group.support == support or 
            support.company == group.support.company and support.is_admin)
        

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

#checked
class IsAgentInstance(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            agent = Agent.get_agent_by_user(request.user)
        except Agent.DoesNotExist:
            return False
        return True


#checked
class IsSupportOrAdminOrSuperAdminRO(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
            return support.is_admin or support.is_operator or \
                   (support.is_superadmin and request.method in permissions.SAFE_METHODS)
        except Support.DoesNotExist:
            return False

#checked
class IsCompanyStuff(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        return support.is_admin or support.is_operator
        

#checked
class IsForThisAgentTask(permissions.BasePermission):
    def has_object_permission(self, request, view, task):
        try: 
            agent = Agent.get_agent_by_user(request.user)
        except Agent.DoesNotExist:
            return False
        if not task.group and task.creater.company == agent.company:
            return True
        if agent.group == task.group:
            return True
        return False


#checked
class IsThisTaskExecuter(permissions.BasePermission):
    def has_object_permission(self, request, view, objtask_filled):
        try: 
            agent = Agent.get_agent_by_user(request.user)
            return task_filled.executer == agent
        except Agent.DoesNotExist:
            return False

#checked
class IsAdminOrAgentOfYourGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        try:
            support = Support.get_support_by_user(request.user)
        except Support.DoesNotExist:
            return False
        return (user.group.support == support 
            or support.is_admin and user.company == support.company)

#checked
class IsThisPayAgent(permissions.BasePermission):
    def has_object_permission(self, request, view, pay):
        try:
            agent = Agent.get_agent_by_user(request.user)
            return pay.agent == agent
        except Agent.DoesNotExist:
            return False