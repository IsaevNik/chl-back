# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..serializers.task_address import TaskWithoutAddressSerializer, \
    TaskWithAddressSerializer
from ...service.task import get_tasks_without_address, get_tasks_with_address
from ...service.agent import get_agent_by_user
from ...service.task_address import is_task_available, get_task_address_by_id, \
    taken_task_by_agent
from ..renderers import JsonRenderer
from api.forms import TaskDistanceForm
from ...utils.exceptions.commons import RequestValidationException
from api.permissions import IsForThisAgentTask, IsAgentInstance


class WithoutAddressTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        tasks = get_tasks_without_address(request.user)
        serializer = TaskWithoutAddressSerializer(tasks, many=True)
        return Response(serializer.data)


class WithAddressTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        form = TaskDistanceForm(request.GET)
        if form.is_valid():
            tasks = get_tasks_with_address(form.cleaned_data, request.user)
            tasks.sort(key=lambda task: task.distance)
            serializer = TaskWithAddressSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            raise RequestValidationException(form)


class TaskForAgentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsForThisAgentTask)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        task_address = get_task_address_by_id(id)
        task = task_address.task
        self.check_object_permissions(self.request, task)
        is_task_available(task_address)

        serializer = TaskWithAddressSerializer(task_address)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, id):
        task_address = get_task_address_by_id(id)
        agent = get_agent_by_user(request.user)
        task = task_address.task
        self.check_object_permissions(self.request, task)
        is_task_available(task_address)

        taken_task_by_agent(task_address ,agent)
        return Response()



