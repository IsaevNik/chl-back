# coding=utf-8
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.subscription_type import SubscriptionTypeSerializer
from ...service.subscription_type import get_all_subscriptions
from api.permissions import IsAdmin, IsAdminOrGroupSupport
from ..renderers import JsonRenderer
from ...utils.exceptions.commons import RequestValidationException

class SubscriptionTypeListView(APIView):
	
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    def get(self, request):
        subscriptions = get_all_subscriptions()
        serializer = SubscriptionTypeSerializer(subscriptions, many=True)
        return Response(serializer.data)

