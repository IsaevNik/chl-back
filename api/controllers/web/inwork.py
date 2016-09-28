# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..renderers import JsonRenderer
from api.permissions import IsAdminOrGroupSupport, IsAdminOrAgentOfYourGroup, \
    IsCompanyStuff, IsCompanyActive
from ...service.support import get_support_by_user
from ...service.task_filled import get_task_inwork_by_status, get_stat_inwork, \
    get_task_filled_by_id, check_task
from ..serializers.task_filled import TaskFilledListWebSerializer, TaskFilledDetailWebSerializer, \
    CheckingTaskSerializer
from api.utils.exceptions.inwork import TaskNotDoneException, TaskMustNotBeCheckingException
from ...utils.exceptions.commons import RequestValidationException


class InWorkTasksListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCompanyStuff, IsCompanyActive)
    renderer_classes = (JsonRenderer,)

    def get(self, request, status):
        support = get_support_by_user(request.user)
        inworks = get_task_inwork_by_status(status, support)
        serializer = TaskFilledListWebSerializer(inworks, many=True)
        return Response(serializer.data)


class InWorkStatsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCompanyStuff, )
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        support = get_support_by_user(request.user)
        inworks_stat = get_stat_inwork(support)
        return Response(inworks_stat)


class InWorkTaskDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrAgentOfYourGroup, IsCompanyActive)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        task_filled = get_task_filled_by_id(id)
        agent = task_filled.executer
        self.check_object_permissions(self.request, agent)

        if task_filled.status == 0:
            raise TaskNotDoneException()
        serializer = TaskFilledDetailWebSerializer(task_filled)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, id):
        task_filled = get_task_filled_by_id(id)
        agent = task_filled.executer
        self.check_object_permissions(self.request, agent)

        if task_filled.status != 1:
            raise TaskMustNotBeCheckingException()

        serializer = CheckingTaskSerializer(data=request.data)
        if serializer.is_valid():
            check_task(task_filled, serializer, request.user)
        else:
            raise RequestValidationException(serializer)
        return Response()


class InWorkHistoryView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCompanyStuff, )
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        support = get_support_by_user(request.user)
        succsess_tasks = get_task_inwork_by_status(3, support)
        fail_tasks = get_task_inwork_by_status(4, support)
        history = (succsess_tasks | fail_tasks).order_by('-check_dt')
        serializer = TaskFilledListWebSerializer(history, many=True)
        return Response(serializer.data)
