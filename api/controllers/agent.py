# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..service.agent import create_agent_start, get_agent, delete_agent, \
    update_agent, get_agent_by_user, get_all_agents, is_first_auth, set_agent_device
from ..service.support import get_support_by_user
from ..service.base_service import logout_user, auth_user, get_user_by_token
from ..service.user_group import get_all_groups_of_company
from ..service.user_group import get_group
from ..service.task import get_start_task_by_company
from api.permissions import IsAdminOrReadOnly, IsSupport, IsAdmin, \
    IsAdminOrGroupSupport, IsSuperAdmin
from .serializers.agent import CreateAgentStartSerializer, AgentSerializer, \
    GroupWithAgentsSerializer, AuthAgentSerializer, FirstAuthAgentSerializer
from ..utils.exceptions.commons import RequestValidationException
from .renderers import JsonRenderer
from api.models.support import Support


class LoginAgentView(APIView):
    """
    Авторизация агента
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    @transaction.atomic
    def post(request):
        serializer = AuthAgentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():

            token = auth_user(serializer.validated_data['login'], 
                                 serializer.validated_data['password'])
            agent = get_agent_by_user(get_user_by_token(token))
            if is_first_auth(agent):
                serializer = FirstAuthAgentSerializer(data=request.data)
                if serializer.is_valid():
                    start_task = get_start_task_by_company(agent.company)
                    data = set_agent_device(agent, serializer, start_task)
                else:
                    raise RequestValidationException(serializer)
            data['token'] = token

            return Response(data)
        else:
            raise RequestValidationException(serializer)


class AgentListView(APIView):
    """
    Первый этап создания объекта Agent
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        serializer = CreateAgentStartSerializer(data=request.data)
        request_user = request.user
        if serializer.is_valid():
            group_id = serializer.validated_data['group_id']
            group = get_group(group_id, request.user)
            self.check_object_permissions(self.request, group)
            user_data = create_agent_start(serializer, request_user)
            #TODO можно ли создавать агентов, если нет стартового задания?
            return Response(user_data)
        else:
            raise RequestValidationException(serializer)

    def get(self, request):
        request_user = request.user
        support = get_support_by_user(request_user)
        if support.is_superadmin:
            agents = get_all_agents()
            serializer = AgentSerializer(agents, many=True)
            return Response(serializer.data)
        else:
            groups = get_all_groups_of_company(request_user)
            serializer = GroupWithAgentsSerializer(groups, many=True)
            return Response(serializer.data)


class AgentDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        agent = get_agent(id, request.user)
        group = agent.group
        self.check_object_permissions(self.request, group)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    def delete(self, request, id):
        agent = get_agent(id, request.user)
        group = agent.group
        self.check_object_permissions(self.request, group)
        delete_agent(agent)
        return Response()

    @transaction.atomic
    def put(self, request, id):
        serializer = CreateAgentStartSerializer(data=request.data)
        agent = get_agent(id, request.user)
        old_group = agent.group
        
        if serializer.is_valid():
            new_group_id = serializer.validated_data['group_id']
            new_group = get_group(new_group_id, request.user)
            self.check_object_permissions(self.request, old_group)
            self.check_object_permissions(self.request, new_group)
            update_agent(agent, serializer, new_group)
            return Response()
        else:
            raise RequestValidationException(serializer)


class AgentProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get( request):
        agent = get_agent_by_user(request.user)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)


class LogoutAgentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        logout_user(request.user)
        return Response()    