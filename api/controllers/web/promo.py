# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.promo import PromoCreateSerializer, PromoListSerializer, \
    PromoDetailSerializer
from api.service.promo import create_promo, get_all_promo_of_company, \
    get_promo_by_id
from api.permissions import IsAdminOrReadOnly, IsThisCompanyObject, \
    IsCompanyActiveOrReadOnly
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException


class PromoListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly, IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        serializer = PromoCreateSerializer(data=request.data)
        if serializer.is_valid():
            create_promo(serializer, request.user)
            return Response()
        else:
            raise RequestValidationException(serializer)

    def get(self, request):
        promos = get_all_promo_of_company(request.user)
        serializer = PromoListSerializer(promos, many=True)
        return Response(serializer.data)


class PromoDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly, IsThisCompanyObject, 
        IsCompanyActiveOrReadOnly)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        promo = get_promo_by_id(id)
        self.check_object_permissions(self.request, promo)
        serializer = PromoDetailSerializer(promo)
        return Response(serializer.data)

    def delete(self, request, id):
        promo = get_promo_by_id(id)
        self.check_object_permissions(self.request, promo)
        delete_promo(promo)
        return Response()

    def put(self, request, id):
        promo = get_promo_by_id(id)
        self.check_object_permissions(self.request, promo)
        serializer = PromoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(promo, serializer.validated_data)
            return Response()
        else:
            raise RequestValidationException(serializer)