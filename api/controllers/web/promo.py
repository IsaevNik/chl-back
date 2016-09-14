# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.promo import PromoCreateSerializer, PromoSerializer
from api.service.promo import create_promo, get_all_promo_of_company
from api.permissions import IsAdmin, IsAdminOrGroupSupportAndReadOnly, IsAdminOrReadOnly
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException


class PromoListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupportAndReadOnly)
    renderer_classes = (JsonRenderer,)

    @staticmethod
    def post(request):
        serializer = PromoCreateSerializer(data=request.data)
        if serializer.is_valid():
            create_promo(serializer, request.user)
            return Response()
        else:
            raise RequestValidationException(serializer)

    @staticmethod
    def get(request):
        promos = get_all_promo_of_company(request.user)
        serializer = PromoSerializer(promos, many=True)
        return Response(serializer.data)


'''class UserGroupDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupportAndReadOnly)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        group = get_group(id, request.user)
        self.check_object_permissions(self.request, group)
        serializer = UserGroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, id):
        group = get_group(id, request.user)
        self.check_object_permissions(self.request, group)
        serializer = UserGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            update_group(group, serializer, request.user)
            return Response()
        else:
            raise RequestValidationException(serializer)

    def delete(self, request, id):
        group = get_group(id, request.user)
        self.check_object_permissions(self.request, group)
        delete_group(group)
        return Response()'''