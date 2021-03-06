# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ...service.agent import create_agent_start, get_agent_by_id, delete_agent, \
    update_agent, get_agent_by_user, get_all_agents
from ...service.support import get_support_by_user
from ...service.user_group import get_all_groups_of_company
from ...service.user_group import get_group_by_id
from api.permissions import IsAdminOrGroupSupport, IsSuperAdmin, \
    IsSupportOrAdminOrSuperAdminRO, IsCompanyActiveOrReadOnly
from ..serializers.agent import CreateAgentStartSerializer, AgentListSerializer, \
    GroupWithAgentsSerializer, AgentDetailSerializer
from ...utils.exceptions.commons import RequestValidationException
from ..renderers import JsonRenderer
from api.models.support import Support


class AgentListView(APIView):
    """
    Первый этап создания объекта Agent
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupportOrAdminOrSuperAdminRO, \
                          IsAdminOrGroupSupport, IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        serializer = CreateAgentStartSerializer(data=request.data)
        request_user = request.user
        if serializer.is_valid():
            group_id = serializer.validated_data['group_id']
            group = get_group_by_id(group_id)
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
            serializer = AgentListSerializer(agents, many=True)
            return Response(serializer.data)
        else:
            groups = get_all_groups_of_company(request_user)
            serializer = GroupWithAgentsSerializer(groups, many=True)
            return Response(serializer.data)


class AgentDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        agent = get_agent_by_id(id)
        self.check_object_permissions(self.request, agent.group)
        serializer = AgentDetailSerializer(agent)
        return Response(serializer.data)

    def delete(self, request, id):
        agent = get_agent_by_id(id)
        self.check_object_permissions(self.request, agent.group)
        delete_agent(agent)
        return Response()

    @transaction.atomic
    def put(self, request, id):
        serializer = CreateAgentStartSerializer(data=request.data)
        agent = get_agent_by_id(id)
        old_group = agent.group
        
        if serializer.is_valid():
            new_group_id = serializer.validated_data['group_id']
            new_group = get_group_by_id(new_group_id)
            self.check_object_permissions(self.request, old_group)
            self.check_object_permissions(self.request, new_group)
            update_agent(agent, serializer, new_group)
            return Response()
        else:
            raise RequestValidationException(serializer)

