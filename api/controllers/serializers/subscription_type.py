# coding: utf-8
from rest_framework import serializers

from api.models.subscription_type import SubscriptionType


class SubscriptionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionType
        fields = ('id', 'title', 'description', 'task_limit', 'support_limit', \
                  'user_limit', 'time', 'price')

