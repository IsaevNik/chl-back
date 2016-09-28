# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..renderers import JsonRenderer
from ...service.agent import get_agent_by_user
from ...service.pay import create_pay, get_pays_by_agent, get_pay_by_id
from api.permissions import IsThisPayAgent, IsAgentInstance
from ..serializers.pay import PayListMobileSerializer, PayDetailMobileSerializer


class PayListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAgentInstance)
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
    permission_classes = (IsAuthenticated, IsAgentInstance, IsThisPayAgent)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        pay = get_pay_by_id(id)
        self.check_object_permissions(self.request, pay)

        serializer = PayDetailMobileSerializer(pay)
        return Response(serializer.data)






