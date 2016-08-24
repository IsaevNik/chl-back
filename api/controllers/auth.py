# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.auth import auth
from ..service.support import create_support_start
from api.permissions import IsAdminOrReadOnly
from .serializers.auth import AuthSerializer
from .serializers.support import SupportSerializer, CreateSupportSerializer
from ..utils.exceptions.commons import RequestValidationException
from .renderers import JsonRenderer
from api.models.support import Support


class AuthView(APIView):
    """
    Авторизация
    """
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            token = auth(serializer.validated_data['email'], serializer.validated_data['password'])
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
        serializer = CreateSupportSerializer(data=request.data)
        request_user = request.user
        if serializer.is_valid():
            token = create_support_start(serializer, request_user)
            return Response({'token': token})
        else:
            raise RequestValidationException(serializer)



class SupportView(APIView):
    """
    Представление Support
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def get(request):
        supports = Support.objects.all()
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data)
