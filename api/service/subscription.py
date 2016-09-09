# coding=utf-8
from datetime import datetime
import urllib2
import urllib

from rest_framework.exceptions import NotFound

from api.models.subscription import Subscription
from api.models.subscription_type import SubscriptionType
from api.models.company import Company
from base_service import get_object


def create_subscription(serializer, support):
    data = serializer.validated_data
    if support.is_booker:
        data['status'] = 2
        company_id = data.get('company_id', 0)
        data['start_dt'] = datetime.now()
    if support.is_admin:
        company_id = support.company.id
    company = get_object(Company, company_id)

    subscription_type_id = data.get('subscription_type_id', 0)
    subscription_type = get_object(SubscriptionType, subscription_type_id)
    
    sub_id = serializer.create(data, company, subscription_type)
    if support.is_admin:
        return sub_id 

def get_all_subscriptions(support):
    if support.is_booker or support.is_superadmin:
        subscriptions = Subscription.objects.all().order_by('status','-purchase_dt')
    elif support.is_admin:
        company = support.company
        subscriptions = Subscription.objects.filter(company=company).order_by('status','-purchase_dt')
    else:
        subscriptions = None
    return subscriptions


def create_payonline_link(sub_id):
    link = 'https://payonline.com?order_id={}'.format(sub_id)
    return link


def get_subscription_by_id(sub_id, support):
    subscription = get_object(Subscription, sub_id)
    if support.is_admin:
        if subscription.company != support.company:
            raise NotFound
    return subscription


def check_transaction(order_id):
    url = 'http://volstelecom.ru'
    """user = ''
    password = ''

    values = {'order_id' : order_id,
             'user' : user,
             'password' : password }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)"""
    response = urllib2.urlopen(url)
    return response