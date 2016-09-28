# coding=utf-8
import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..serializers.task_filled import TaskFilledUpdateSerializer, \
    TaskFilledListMobileSerializer
from ...service.agent import get_agent_by_user
from ...service.task_filled import do_the_task, cancel_the_task, \
    get_task_inwork_by_status, get_task_inwork_by_user, get_task_filled_by_id
from ...service.task import get_point_blanks_by_task
from ..serializers.point_blank import PointBlankSerializer
from api.permissions import IsThisTaskExecuter, IsAgentInstance
from api.forms import TaskDistanceForm
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException
from ...utils.exceptions.inwork import CancelTaskException, DoTaskException


class BlanksOfTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsThisTaskExecuter)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        task_filled = get_task_filled_by_id(id)
        self.check_object_permissions(self.request, task_filled)

        point_blanks = get_point_blanks_by_task(task_filled.task_address.task)
        serializer = PointBlankSerializer(point_blanks, many=True)
        return Response(serializer.data)


class InWorkTaskDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsThisTaskExecuter)
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request, id):
        task_filled = get_task_filled_by_id(id)
        self.check_object_permissions(self.request, task_filled)
        if task_filled.status != 0:
            raise DoTaskException()

        serializer = TaskFilledUpdateSerializer(data=request.data)
        if serializer.is_valid():
            do_the_task(request, task_filled, serializer)
            return Response()
        else:
            raise RequestValidationException(serializer)

    @transaction.atomic
    def delete(self, request, id):
        task_filled = get_task_filled_by_id(id)
        self.check_object_permissions(self.request, task_filled)
        if task_filled.status != 0:
            raise CancelTaskException()

        cancel_the_task(task_filled)
        return Response()

    def get(self, request, id):
        form = TaskDistanceForm(request.GET)
        task_filled = get_task_filled_by_id(id)
        self.check_object_permissions(self.request, task_filled)
        if form.is_valid():
            if task_filled.task_address.latitude:
                task_filled.task_address.set_distance(form.cleaned_data['longitude'], 
                                                      form.cleaned_data['latitude'])
            serializer = TaskFilledListMobileSerializer(task_filled)
            return Response(serializer.data)
        else:
            raise RequestValidationException(form)
         

class InWorkTasksByStatusListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request, status):
        agent = get_agent_by_user(request.user)
        inworks = get_task_inwork_by_status(status, agent)
        serializer = TaskFilledListMobileSerializer(inworks, many=True)
        return Response(serializer.data)


class InWorkAgentsTaskListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        form = TaskDistanceForm(request.GET)
        agent = get_agent_by_user(request.user)

        if form.is_valid():
            inworks = get_task_inwork_by_user(agent, form.cleaned_data)
            serializer = TaskFilledListMobileSerializer(inworks, many=True)
            return Response(serializer.data)
        else:
            raise RequestValidationException(form)


class InWorkAgentsHistoryListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        agent = get_agent_by_user(request.user)
        succsess_tasks = get_task_inwork_by_status(3, agent)
        fail_tasks = get_task_inwork_by_status(4, agent)
        history = (succsess_tasks | fail_tasks).order_by('-check_dt')
        serializer = TaskFilledListMobileSerializer(history, many=True)
        return Response(serializer.data)
      
       
        