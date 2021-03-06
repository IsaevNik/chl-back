# coding=utf-8
import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect

from ..serializers.task import TaskCreateSerializer, GroupWithTaskSerializer, \
    TaskDetailSerializer
from ..serializers.task_address import TaskAddressCreateSerializer
from ..serializers.point_blank import PoinBlankCreateSerializer
from api.forms import JsonReqForm
from ...service.task import get_data_for_task, create_task, get_task_by_id, \
    update_task, get_start_task_by_company
from ...service.user_group import get_group_by_id
from ...service.support import get_support_by_user, get_all_groups_of_support
from ...service.task_address import create_task_address, update_task_address, \
    delete_task_addresses
from ...service.point_blank import create_blank, update_blank, delete_blanks
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException
from ...utils.exceptions.task import WithoutGroupTaskCreateException, \
    StartTaskWithGroupException, StartTaskCreateException, StartTaskDeleteException
from api.permissions import IsAdminOrGroupSupport, IsAdminOrReadOnly, \
    IsCompanyStuff, IsCompanyActiveOrReadOnly, IsSupportTask


class TaskListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCompanyStuff, \
                          IsAdminOrGroupSupport, IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        form = JsonReqForm(request.data)
        if not form.is_valid():
            raise RequestValidationException(form)
        json_task = json.loads(form.cleaned_data['task'])
        data_for_task = get_data_for_task(json_task, request.user)

        support = get_support_by_user(request.user)

        #Если указан идентификатор группы, проверить наличие прав на эту группу
        if data_for_task['group_id']:
            group = get_group_by_id(data_for_task['group_id'])
            self.check_object_permissions(self.request, group)
        else:
            raise WithoutGroupTaskCreateException()

        task_serializer = TaskCreateSerializer(data=data_for_task)

        if not task_serializer.is_valid():
            raise RequestValidationException(task_serializer)

        task = create_task(task_serializer, support, group)

        # работа с адресами
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address)
            if ta_serializer.is_valid():
                create_task_address(ta_serializer, task, support)
            else:
                raise RequestValidationException(ta_serializer)

        # работа с бланками заданий
        for json_blank in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_blank)
            if b_serializer.is_valid():
                create_blank(b_serializer, task)
            else:
                raise RequestValidationException(b_serializer)

        return Response()

    def get(self, request):
        support = get_support_by_user(request.user)
        groups = get_all_groups_of_support(support)
        serializer = GroupWithTaskSerializer(groups, many=True)
        return Response(serializer.data)


class StartTaskView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,\
                          IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        support = get_support_by_user(request.user)
        company = support.company
        start_task = get_start_task_by_company(company)
        if start_task:
            serializer = TaskDetailSerializer(start_task)
            return Response(serializer.data)
        else:
            return Response()

    @transaction.atomic
    def post(self, request):
        form = JsonReqForm(request.data)
        if not form.is_valid():
            raise RequestValidationException(form)

        support = get_support_by_user(request.user)

        json_task = json.loads(form.cleaned_data['task'])
        data_for_task = get_data_for_task(json_task, request.user)
        data_for_task['is_start'] = 1
        task_serializer = TaskCreateSerializer(data=data_for_task)

        if not task_serializer.is_valid():
            raise RequestValidationException(task_serializer)

        task = create_task(task_serializer, support, None)

        # работа с адресами
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address)
            if ta_serializer.is_valid():
                create_task_address(ta_serializer, task, support)
            else:
                raise RequestValidationException(ta_serializer)

        # работа с бланками заданий
        for json_blank in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_blank)
            if b_serializer.is_valid():
                create_blank(b_serializer, task)
            else:
                raise RequestValidationException(b_serializer)

        return Response()

    @transaction.atomic
    def put(self, request):
        support = get_support_by_user(request.user)
        task = get_start_task_by_company(support.company)

        form = JsonReqForm(request.data)
        if not form.is_valid():
            raise RequestValidationException(form)
        json_task = json.loads(form.cleaned_data['task'])
        data_for_task = get_data_for_task(json_task, request.user)

        task_serializer = TaskCreateSerializer(data=data_for_task)
        if not task_serializer.is_valid():
            raise RequestValidationException(task_serializer)
        #проверяем валидность данных для адресов заданий и записываем в массив 
        #идентификаторы заданий которые остались из старой версии задания
        ta_ids = []
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address)
            if ta_serializer.is_valid():
                id = ta_serializer.validated_data['id']
                if id:
                    ta_ids.append(id)
            else:
                raise RequestValidationException(ta_serializer)
        #проверяем валидность данных для бланков заданий и записываем в массив 
        #идентификаторы бланков которые остались из старой версии задания
        b_ids = []
        for json_address in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_address)
            if b_serializer.is_valid():
                id = b_serializer.validated_data['id']
                if id:
                    b_ids.append(id)
            else:
                raise RequestValidationException(b_serializer)
        #проверка прав на новую группу    
        data_for_task['is_start'] = 1

        task = update_task(task_serializer, task, support, None)

        #удалить адреса, которые были в предыдущей версии и их нет сейчас
        delete_task_addresses(ta_ids)

        #работа с адресами задания
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address) 
            if ta_serializer.is_valid():
                update_task_address(ta_serializer, task, ta_ids)

        #удалить бланки, которые были в предыдущей версии и их нет сейчас
        delete_blanks(b_ids)

        # работа с бланками заданий
        for json_blank in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_blank)
            if b_serializer.is_valid():
                update_blank(b_serializer, task, b_ids)

        return Response()


class TaskDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCompanyStuff, \
                          IsSupportTask, IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)


    def get(self, request, id):
        support = get_support_by_user(request.user)
        task = get_task_by_id(id)
        
        self.check_object_permissions(self.request, task)
        if task.is_start:
            return redirect('/api/web/tasks/start/')
        
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


    @transaction.atomic
    def put(self, request, id):
        support = get_support_by_user(request.user)
        task = get_task_by_id(id)

        self.check_object_permissions(self.request, task)

        form = JsonReqForm(request.data)
        if not form.is_valid():
            raise RequestValidationException(form)
        json_task = json.loads(form.cleaned_data['task'])
        data_for_task = get_data_for_task(json_task, request.user)

        task_serializer = TaskCreateSerializer(data=data_for_task)
        if not task_serializer.is_valid():
            raise RequestValidationException(task_serializer)

        
        #проверка прав на новую группу    
        new_group = get_group_by_id(task_serializer.validated_data['group_id'])
        if new_group:
            if not (new_group.support == support or 
                new_group.support.company == support.company and support.is_admin):
                raise PermissionDenied()
        else:
            #TODO redirect если задание вводное
            return redirect('/api/web/tasks/start/')
            raise PermissionDenied()

        #проверяем валидность данных для адресов заданий и записываем в массив 
        #идентификаторы заданий которые остались из старой версии задания
        ta_ids = []
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address)
            if ta_serializer.is_valid():
                id = ta_serializer.validated_data['id']
                if id:
                    ta_ids.append(id)
            else:
                raise RequestValidationException(ta_serializer)
        #проверяем валидность данных для бланков заданий и записываем в массив 
        #идентификаторы бланков которые остались из старой версии задания
        b_ids = []
        for json_address in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_address)
            if b_serializer.is_valid():
                id = b_serializer.validated_data['id']
                if id:
                    b_ids.append(id)
            else:
                raise RequestValidationException(b_serializer)

        task = update_task(task_serializer, task, support, new_group)

        #удалить адреса, которые были в предыдущей версии и их нет сейчас
        delete_task_addresses(ta_ids)

        #работа с адресами задания
        for json_address in json_task['addresses']:
            ta_serializer = TaskAddressCreateSerializer(data=json_address) 
            if ta_serializer.is_valid():
                update_task_address(ta_serializer, task, ta_ids)

        #удалить бланки, которые были в предыдущей версии и их нет сейчас
        delete_blanks(b_ids)

        # работа с бланками заданий
        for json_blank in json_task['blanks']:
            b_serializer = PoinBlankCreateSerializer(data=json_blank)
            if b_serializer.is_valid():
                update_blank(b_serializer, task, b_ids)

        return Response()


    def delete(self, request, id):
        support = get_support_by_user(request.user)
        task = get_task_by_id(id)

        self.check_object_permissions(self.request, task)
        if task.is_start:
            raise StartTaskDeleteException()
        task.delete()
        return Response()


