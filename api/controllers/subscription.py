# coding=utf-8
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, renderer_classes, \
    permission_classes

from .serializers.subscription import SubscriptionSerializer, \
    CreateSubscriptionSerializer
from ..service.subscription import create_subscription, get_all_subscriptions, \
    create_payonline_link, get_subscription_by_id, check_transaction
from ..service.support import get_support_by_user
from api.permissions import IsAdmin, IsAdminOrGroupSupport, IsAdminOrBooker
from .renderers import JsonRenderer
from ..utils.exceptions.commons import RequestValidationException
from ..utils.exceptions.pay import OrderNotExistException


class SubscriptionListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrBooker)
    renderer_classes = (JsonRenderer,)

    def post(self, request):
        support = get_support_by_user(request.user)
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            sub_id = create_subscription(serializer, support)
            if sub_id:
                link = create_payonline_link(sub_id)
                return Response({'link': link})
            else:
                return Response()
        else: 
            raise RequestValidationException(serializer)

    
    def get(self, request):
        support = get_support_by_user(request.user)
        subscriptions = get_all_subscriptions(support)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

class SubscriptionDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrBooker)
    renderer_classes = (JsonRenderer,)

    def get(self, request, id):
        support = get_support_by_user(request.user)
        subscription = get_subscription_by_id(id, support)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    '''def put(self, request, id):
        support = get_support_by_user(request.user)
        subscription = get_subscription_by_id(id, support)
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():'''

@api_view(['GET'])
@renderer_classes([JsonRenderer])
@permission_classes([])
def put_order_id(request):
    order_id = request.GET.get('order_id', None)
    if order_id:
        response = check_transaction(order_id)
    else:
        raise OrderNotExistException

    return Response()
