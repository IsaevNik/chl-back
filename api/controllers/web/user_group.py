# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user_group import UserGroupListSerializer, UserGroupCreateSerializer, \
    UserGroupDetailSerializer
from ...service.user_group import create_group, get_all_groups_of_company, update_group, \
    delete_group, get_group_by_id
from api.permissions import IsAdmin, IsAdminOrGroupSupportAndReadOnly, IsAdminOrReadOnly
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException


class UserGroupListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        serializer = UserGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            create_group(serializer, request.user)
            return Response()
        else:
            raise RequestValidationException(serializer)

    def get(self, request):
        groups = get_all_groups_of_company(request.user)
        serializer = UserGroupListSerializer(groups, many=True)
        return Response(serializer.data)


class UserGroupDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrGroupSupportAndReadOnly)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        group = get_group_by_id(id, request.user)
        self.check_object_permissions(self.request, group)
        serializer = UserGroupDetailSerializer(group)
        return Response(serializer.data)

    def put(self, request, id):
        group = get_group_by_id(id, request.user)
        self.check_object_permissions(self.request, group)
        serializer = UserGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            update_group(group, serializer, request.user)
            return Response()
        else:
            raise RequestValidationException(serializer)

    def delete(self, request, id):
        group = get_group_by_id(id, request.user)
        self.check_object_permissions(self.request, group)
        delete_group(group)
        return Response()