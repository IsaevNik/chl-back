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
from ...service.company import create_company_start, update_company, get_all_company, \
    get_company_by_id
from ...service.support import create_support_finish, get_support_by_user,\
    is_support
from api.permissions import IsAdminOrReadOnly, IsSuperAdmin, IsCompanyActiveOrReadOnly
from ..renderers import JsonRenderer


class CompanyView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly, IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        user = request.user
        support = get_support_by_user(user)
        serializer = CompanyFullSerializer(support.company)
        return Response(serializer.data)

    def put(self, request):
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

    def get(self, request):
        companies = get_all_company()
        serializer = CompanyPartSerializer(companies, many=True)
        return Response(serializer.data)


class CompanyDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperAdmin)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        companies = get_company_by_id(id)
        serializer = CompanyFullSerializer(companies)
        return Response(serializer.data)


class RegCompanyStartView(APIView):

    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        serializer = RegCompanyStartSerializer(data=request.data)
        if serializer.is_valid():
            token = create_company_start(serializer)
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)

