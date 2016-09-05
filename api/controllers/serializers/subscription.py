# coding: utf-8
from rest_framework import serializers

from api.models.subscription import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    company = serializers.CharField(source='company.name')
    subscription_type = serializers.CharField(source='subscription_type.title')
    end_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    purchase_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Subscription
        fields = ('id', 'company', 'subscription_type', 'status', 'purchase_dt',\
         'start_dt', 'end_dt')

    def get_status(self,obj):
        return obj.get_status_display()

class CreateSubscriptionSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=1)
    company_id = serializers.IntegerField(required=False)
    subscription_type_id = serializers.IntegerField()

    def create(self, data, company, subscription_type):
        subscription = Subscription(
            company=company,
            start_dt=data.get('start_dt', None),
            status=data['status'],
            subscription_type=subscription_type
            )
        subscription.save()
        return subscription.id

