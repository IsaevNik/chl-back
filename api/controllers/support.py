# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from ..service.support import create_support_start, create_support_finish, \
     update_support, get_all_supports_of_company, get_support, \
     delete_support, get_support_by_user
from ..service.base_service import logout_user, auth_user
from api.permissions import IsAdminOrReadOnly, IsSupport, IsAdmin
from .serializers.support import SupportSerializer, CreateSupportStartSerializer, \
    CreateSupportFinishSerializer, AuthSupportSerializer
from ..utils.exceptions.commons import RequestValidationException
from .renderers import JsonRenderer
from api.models.support import Support


class AuthSupportView(APIView):
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
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    renderer_classes = (JsonRenderer,)

    @staticmethod

    def post(request):
        serializer = CreateSupportStartSerializer(data=request.data)
        request_user = request.user
        if serializer.is_valid():
            token = create_support_start(serializer, request_user)
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

    @staticmethod
    @transaction.atomic
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
    @transaction.atomic
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

    @staticmethod
    def post(request):
        logout_user(request.user)
        return Response()