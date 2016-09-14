# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.db import transaction

from ..serializers.company import CompanyFullSerializer, CompanyPartSerializer, \
    RegCompanyStartSerializer, CompanyUpdateSerializer
from ..serializers.support import CreateSupportFinishSerializer
from ...utils.exceptions.commons import RequestValidationException
from ...service.base_service import get_all, get_object
from ...service.company import create_company_start, update_company, get_all_company
from ...service.support import create_support_finish, get_support_by_user,\
    is_support
from api.permissions import IsAdminOrReadOnly, IsSuperAdmin
from ..renderers import JsonRenderer


class CompanyView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        user = request.user
        if is_support(user):
            support = get_support_by_user(user)
            serializer = CompanyFullSerializer(support.company)
            return Response(serializer.data)
        else:
            #TODO для пользователей предоставить минимальную инфу о компании 
            #(возможно тут как раз будет лого и тд)
            raise PermissionDenied()

    @staticmethod
    def put(request):
        support = get_support_by_user(request.user)
        company = support.company
        serializer = CompanyUpdateSerializer(data=request.data)
        if serializer.is_valid():
            update_company(company, serializer)
            return Response()
        else:
            raise RequestValidationException(serializer)


class CompanyStatisticView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperAdmin)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        companies = get_all_company()
        serializer = CompanyFullSerializer(companies, many=True)
        return Response(serializer.data)


class RegCompanyStartView(APIView):

    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        serializer = RegCompanyStartSerializer(data=request.data)
        if serializer.is_valid():
            token = create_company_start(serializer)
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)


class RegCompanyFinishView(APIView):

    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    @transaction.atomic
    def post(request):
        serializer = CreateSupportFinishSerializer(data=request.data)
        if serializer.is_valid():
            create_support_finish(serializer, is_admin=True)
            return Response()
        else:
            raise RequestValidationException(serializer)