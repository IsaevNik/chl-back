# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.agent import create_agent_start, get_agent, delete_agent, \
    update_agent
from ..service.support import get_support_by_user
from ..service.user_group import get_all_groups_of_company
from ..service.user_group import get_group
from api.permissions import IsAdminOrReadOnly, IsSupport, IsAdmin, IsAdminOrGroupSupport
from .serializers.agent import CreateAgentStartSerializer, AgentSerializer, \
    GroupWithAgentsSerializer
from ..utils.exceptions.commons import RequestValidationException
from .renderers import JsonRenderer
from api.models.support import Support


'''class AuthSupportView(APIView):
    """
    Авторизация
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        serializer = AuthSupportSerializer(data=request.data)
        if serializer.is_valid():
            token = auth_support(serializer.validated_data['email'], 
                                 serializer.validated_data['password'])
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)'''


class AgentListView(APIView):
    """
    Первый этап создания объекта Agent
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        print request.data
        print request.POST
        serializer = CreateAgentStartSerializer(data=request.data)
        request_user = request.user
        if serializer.is_valid():
            group_id = serializer.validated_data['group_id']
            group = get_group(group_id, request.user)
            self.check_object_permissions(self.request, group)
            user_data = create_agent_start(serializer, request_user)
            return Response(user_data)
        else:
            raise RequestValidationException(serializer)

    def get(self, request):
        request_user = request.user
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

'''class CreateSupportFinishView(APIView):
    """
    Второй этап создания объекта Support
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        serializer = CreateSupportFinishSerializer(data=request.data)
        if serializer.is_valid():
            create_support_finish(serializer)
            return Response()
        else:
            raise RequestValidationException(serializer)


class SupportListView(APIView):
    """
    Представление списка Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        supports = get_all_supports_of_company(request.user)
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data)

'''
"""
class SupportDetailView(APIView):
    '''
    Представление объекта Support
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request, id):
        support = get_support(id, request.user)
        serializer = SupportSerializer(support)
        return Response(serializer.data)

    @staticmethod
    def delete(request, id):
        support = get_support(id, request.user)
        delete_support(support)
        return Response()

    @staticmethod
    def put(request, id):
        support = get_support(id, request.user)
        serializer = CreateSupportStartSerializer(data=request.data)
        if serializer.is_valid():
            update_support(support, serializer)
            return Response()
        else:
            raise RequestValidationException(serializer)



class SupportProfileView(APIView):
    '''
    Работа оператора со своим профилем
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        support = get_support_by_user(request.user)
        serializer = SupportSerializer(support)
        return Response(serializer.data)

"""