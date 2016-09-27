# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ...service.agent import get_agent_by_user, is_first_auth, set_agent_device, \
    recover_password_start, recover_password_finish
from ...service.base_service import logout_user, auth_user, get_user_by_token
from ...service.task import get_start_task_by_company
from ..serializers.agent import AgentDetailSerializer, \
    AuthAgentSerializer, FirstAuthAgentSerializer
from ...utils.exceptions.commons import RequestValidationException
from ...utils.exceptions.company import AgentNotFoundException
from ..renderers import JsonRenderer
from api.permissions import IsAgentInstance
from api.forms import RecoverPasswordAgentStartForm, RecoverPasswordAgentFinishForm

class LoginAgentView(APIView):
    """
    Авторизация агента
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        serializer = AuthAgentSerializer(data=request.data)
        response_data = {}
        if serializer.is_valid():

            token = auth_user(serializer.validated_data['login'], 
                                 serializer.validated_data['password'])
            agent = get_agent_by_user(get_user_by_token(token))
            if is_first_auth(agent):
                serializer = FirstAuthAgentSerializer(data=request.data)
                if serializer.is_valid():
                    start_task = get_start_task_by_company(agent.company)
                    response_data = set_agent_device(agent, serializer, start_task)
                else:
                    raise RequestValidationException(serializer)
            response_data['token'] = token

            return Response(response_data)
        else:
            raise RequestValidationException(serializer)


class AgentProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        agent = get_agent_by_user(request.user)
        serializer = AgentDetailSerializer(agent)
        return Response(serializer.data)


class LogoutAgentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        logout_user(request.user)
        return Response()    


class RecoverPasswordStartView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        form = RecoverPasswordAgentStartForm(request.POST)
        if form.is_valid():
            data = recover_password_start(form)
            return Response(data)
        else:
            raise RequestValidationException(form)


class RecoverPasswordFinishView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        form = RecoverPasswordAgentFinishForm(request.POST)
        if form.is_valid():
            token = recover_password_finish(form)
            return Response({'token': token})
        else:
            raise RequestValidationException(form)