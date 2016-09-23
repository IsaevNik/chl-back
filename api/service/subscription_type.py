# coding=utf-8
from api.models.subscription_type import SubscriptionType
from api.utils.exceptions.subscription import SubscriptionTypeNotFoundException


def get_all_subscriptions():
    return SubscriptionType.objects.filter(price__gt=0).order_by('price')

def get_subscription_type_by_id(id):
    try:
        support = SubscriptionType.objects.get(id=id)
    except SubscriptionType.DoesNotExist:
        raise SubscriptionTypeNotFoundException()
    return support