# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..renderers import JsonRenderer
from ...service.support import get_support_by_user
from ...service.pay import create_pay, get_list_of_pay_by_status, \
    get_pay_by_id, check_pay_request
from api.permissions import IsAdminOrGroupSupport, IsSupport
from ..serializers.pay import PaySerializer, PayDetailWebSerializer, \
    PayUpdateSerializer, PayHistoryWebSerializer


class PaysListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport)
    renderer_classes = (JsonRenderer,)
    
    def get(self, request):
        support = get_support_by_user(request.user)
        pays = get_list_of_pay_by_status(support, [0]).order_by('request_dt')
        serializer = PaySerializer(pays, many=True)
        return Response(serializer.data)


class PaysDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupport)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        pay = get_pay_by_id(id)
        self.check_object_permissions(self.request, pay.agent.group)

        serializer = PayDetailWebSerializer(pay)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, id):
        pay = get_pay_by_id(id)
        self.check_object_permissions(self.request, pay.agent.group)

        serializer = PayUpdateSerializer(data=request.data)
        if serializer.is_valid():
            check_pay_request(pay, serializer)
        return Response()


class PaysHistoryListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport)
    renderer_classes = (JsonRenderer,)
    
    def get(self, request):
        support = get_support_by_user(request.user)
        pays = get_list_of_pay_by_status(support, [1,2]).order_by('-check_dt')
        serializer = PayHistoryWebSerializer(pays, many=True)
        return Response(serializer.data)

