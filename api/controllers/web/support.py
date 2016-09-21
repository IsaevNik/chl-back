# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ...service.support import create_support_start, create_support_finish, \
     update_support, get_all_supports_of_company, get_support_by_id, \
     delete_support, get_support_by_user
from ...service.base_service import logout_user, auth_user
from api.permissions import IsAdmin, IsAdminOrSuperAdmin, \
    IsCompanyActive, IsSupportInstance
from ..serializers.support import SupportSerializer, CreateSupportStartSerializer, \
    CreateSupportFinishSerializer, AuthSupportSerializer
from ...utils.exceptions.commons import RequestValidationException
from ..renderers import JsonRenderer
from api.models.support import Support


class LoginSupportView(APIView):
    """
    Авторизация оператора
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        serializer = AuthSupportSerializer(data=request.data)
        if serializer.is_valid():
            token = auth_user(serializer.validated_data['email'], 
                                 serializer.validated_data['password'])
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)


class CreateSupportStartView(APIView):
    """
    Первый этап создания объекта Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin, IsCompanyActive)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        serializer = CreateSupportStartSerializer(data=request.data)
        if serializer.is_valid():
            token = create_support_start(serializer, request.user)
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)


class CreateSupportFinishView(APIView):
    """
    Второй этап создания объекта Support
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @transaction.atomic
    def post(self, request):
        serializer = CreateSupportFinishSerializer(data=request.data)
        if serializer.is_valid():
            token = create_support_finish(serializer)
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)


class SupportListView(APIView):
    """
    Представление списка Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrSuperAdmin)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        supports = get_all_supports_of_company(request.user)
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data)


class SupportDetailView(APIView):
    '''
    Представление объекта Support
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin, IsCompanyActive)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        support = get_support_by_id(id, request.user)
        serializer = SupportSerializer(support)
        return Response(serializer.data)

    def delete(self, request, id):
        support = get_support_by_id(id, request.user)
        delete_support(support)
        return Response()

    @transaction.atomic
    def put(self, request, id):
        support = get_support_by_id(id, request.user)
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
    permission_classes = (IsAuthenticated, IsSupportInstance)
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        support = get_support_by_user(request.user)
        serializer = SupportSerializer(support)
        return Response(serializer.data)


class LogoutSupportView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupportInstance)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        logout_user(request.user)
        return Response()  