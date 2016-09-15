# coding=utf-8
from django.utils import timezone

from ..utils.exceptions.pay import LowBalanceException, PayStatusException, \
    PayAlreadyCheckException
from api.models.pay import Pay
from base_service import get_object


def create_pay(agent):
    group_promo = agent.group.promos
    if group_promo.limit > agent.purse.get_balance():
        raise LowBalanceException()
    pay = Pay.objects.create(agent=agent)


def get_pays_by_agent(agent):
    return Pay.objects.filter(agent=agent).order_by('-request_dt')


def get_pay_by_id(id):
    return get_object(Pay, id)


def get_list_of_pay_by_status(support, status):
    company = support.company

    if support.is_admin:
        pays = Pay.objects.filter(status__in=status, agent__company=company)
    else:
        groups = support.groups
        pays = Pay.objects.filter(status__in=status, agent__group__in=groups.all())
    return pays


def check_pay_request(pay, serializer):
    data = serializer.validated_data
    if pay.status:
        raise PayAlreadyCheckException() 
    if not data['status'] in [1,2]:
        raise PayStatusException()

    group_promo = pay.agent.group.promos

    if data['status'] == 1:
        pay.agent.purse.balance -= group_promo.limit
        pay.agent.purse.save()

    pay.status = data['status']
    pay.check_dt = timezone.now()
    pay.comment = data.get('comment', 'Комментарий отсутствует')
    pay.save()

