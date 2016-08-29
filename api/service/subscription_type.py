# coding=utf-8
from api.models.subscription_type import SubscriptionType

def get_all_subscriptions():
    return SubscriptionType.objects.filter(price__gt=0).order_by('price')