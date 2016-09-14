# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..serializers.task_address import TaskWithoutAddressSerializer, \
    TaskWithAddressSerializer
from ...service.task import get_tasks_without_address, get_tasks_with_address, \
    get_point_blanks_by_task
from ...service.agent import get_agent_by_user
from ...service.task_address import is_task_available, get_task_address, \
    taken_task_by_agent
from ..renderers import JsonRenderer
from api.forms import TaskDistanceForm
from ...utils.exceptions.commons import RequestValidationException
from api.permissions import IsThisGroupMember


class WithoutAddressTaskView(APIView):
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
        return Response()



'''class TaskListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupport, IsSupport)
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
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

        if not support.is_admin and data_for_task['is_start']:
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
        else:
            group = None

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
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        support = get_support_by_user(request.user)
        company = support.company
        start_task = get_start_task_by_company(company)
        if start_task:
            serializer = TaskSerializer(start_task)
            return Response(serializer.data)
        else:
            return Response()


class TaskDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)


    def get(self, request, id):
        support = get_support_by_user(request.user)
        task = get_task(id)
        group = task.group

        if not group and not support.is_admin:
            raise PermissionDenied

        if group:    
            self.check_object_permissions(self.request, group)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request, id):
        support = get_support_by_user(request.user)
        task = get_task(id)
        old_group = task.group

        if not old_group and not support.is_admin:
            raise PermissionDenied
        #проверка прав на старую группу
        if old_group:    
            self.check_object_permissions(self.request, old_group)

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
        new_group = get_group(task_serializer.validated_data['group_id'], request.user)
        if new_group:
            self.check_object_permissions(self.request, new_group)
        else:
            new_group = None

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
        task = get_task(id)
        group = task.group

        if not group and not support.is_admin:
            raise PermissionDenied

        if group:    
            self.check_object_permissions(self.request, group)
        #TODO проверка, если задание вводное, то запретить удаление
        task.delete()
        return Response()'''

