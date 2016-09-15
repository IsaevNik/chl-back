# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..renderers import JsonRenderer
from ...service.agent import get_agent_by_user
from ...service.pay import create_pay, get_pays_by_agent, get_pay_by_id
from api.permissions import IsAgent, IsThisPayAgent
from ..serializers.pay import PayListMobileSerializer, PayDetailMobileSerializer


class PayListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgent)
    renderer_classes = (JsonRenderer,)
    

    def post(self, request):
        agent = get_agent_by_user(request.user)
        create_pay(agent)
        return Response()

    def get(self, request):
        agent = get_agent_by_user(request.user)
        pays = get_pays_by_agent(agent)
        serializer = PayListMobileSerializer(pays, many=True)
        return Response(serializer.data)


class PayDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgent, IsThisPayAgent)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        pay = get_pay_by_id(id)
        self.check_object_permissions(self.request, pay)

        serializer = PayDetailMobileSerializer(pay)
        return Response(serializer.data)


'''class WithoutAddressTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        tasks = get_tasks_without_address(request.user)
        serializer = TaskWithoutAddressSerializer(tasks, many=True)
        return Response(serializer.data)



class WithAddressTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated, IsThisGroupMember)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        task_address = get_task_address(id)
        task = task_address.task
        group = task.group
        self.check_object_permissions(self.request, group)
        is_task_available(task_address)

        serializer = TaskWithAddressSerializer(task_address)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, id):
        task_address = get_task_address(id)
        agent = get_agent_by_user(request.user)
        task = task_address.task
        group = task.group
        self.check_object_permissions(self.request, group)
        is_task_available(task_address)

        taken_task_by_agent(task_address ,agent)
        return Response()'''



