# coding=utf-8
import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers.task import TaskCreateSerializer
from api.forms import JsonReqForm
from ..service.task import get_data_for_task, create_task
from ..service.user_group import get_group
from ..service.support import get_support_by_user
from .renderers import JsonRenderer
from ..utils.exceptions.commons import RequestValidationException
from ..utils.exceptions.task import WithoutGroupTaskCreateException, \
    StartTaskWithGroupException, StartTaskCreateException
from api.permissions import IsAdminOrGroupSupport


class TaskListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        form = JsonReqForm(request.data)
        if not form.is_valid():
            raise RequestValidationException(form)
        json_task = json.loads(form.cleaned_data['task'])
        data_for_task = get_data_for_task(json_task, request.user)

        support = get_support_by_user(request.user)

        #Вводные задания (без определённой группы), может 
        #создавать только админ
        if not support.is_admin and (not data_for_task['group_id']):
            raise WithoutGroupTaskCreateException

        if not support.is_admin and  data_for_task['is_start']:
            raise StartTaskCreateException

        if support.is_admin and (not data_for_task['group_id']) and (not data_for_task['is_start']):
            raise WithoutGroupTaskCreateException


        #для создания вводного задания группу указывать не надо
        if support.is_admin and data_for_task['is_start'] and data_for_task['group_id']:
            raise StartTaskWithGroupException


        #Если указан идентификатор группы, проверить наличие прав на эту группу
        if data_for_task['group_id']:
            group = get_group(data_for_task['group_id'], request.user)
            self.check_object_permissions(self.request, group)

        task_serializer = TaskCreateSerializer(data=data_for_task)

        if not task_serializer.is_valid():
            raise RequestValidationException(task_serializer)

        if data_for_task['group_id']:
            task = create_task(task_serializer, support, group)
        else:
            task = create_task(task_serializer, support)

        return Response()


    def get(self, request):
        pass



class TaskDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JsonRenderer,)


    def get(self, request, id):
        pass

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass