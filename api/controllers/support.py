# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.support import create_support_start, create_support_finish, \
     auth_support
from api.permissions import IsAdminOrReadOnly, IsSupport
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
            token = auth_support(serializer.validated_data['email'], serializer.validated_data['password'])
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)


class CreateSupportStartView(APIView):
    """
    Первый этап создания объекта Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
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
    def post(request):
        serializer = CreateSupportFinishSerializer(data=request.data)
        if serializer.is_valid():
            create_support_finish(serializer)
            return Response()
        else:
            raise RequestValidationException(serializer)


class SupportListView(APIView):
    """
    Представление Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSupport)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        supports = get_all_support()
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data)



