# coding: utf-8
from rest_framework import serializers

from api.models.subscription import Subscription


class SubscriptionListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    end_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Subscription
        fields = ('id', 'company','status', 'end_dt')

    def get_status(self,obj):
        return obj.get_status_display()

    def get_company(self, obj):
        return {"id": obj.company.id, "name": obj.company.name}


class SubscriptionDetailSerializer(SubscriptionListSerializer):
    subscription_type = serializers.SerializerMethodField()
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    purchase_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Subscription
        fields = ('id', 'company', 'subscription_type', 'status', 'purchase_dt',\
         'start_dt', 'end_dt')

    def get_subscription_type(self, obj):
        return {"id": obj.subscription_type.id, "title": obj.subscription_type.title}


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

    def update(self, subscription, data):
        subscription.status = data['status']
        subscription.start_dt = data.get('start_dt', None)
        subscription.save()