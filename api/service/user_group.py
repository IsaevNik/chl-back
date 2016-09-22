# coding=utf-8
from rest_framework.exceptions import NotFound

from api.models.support import Support
from api.models.user_group import UserGroup
from support import get_support_by_id
from base_service import get_object
from promo import get_promo_by_id
from api.utils.exceptions.company import PromoNotFoundException, GroupNotFoundException


def create_group(serializer, user):
    support = get_support_by_id(serializer.validated_data['support_id'], user)
    promo = get_promo_by_id(serializer.validated_data['promo_id'])
    if promo.company != support.company:
        raise PromoNotFoundException()
    serializer.create(serializer.validated_data, support=support, promo=promo)

def get_all_groups_of_company(user):
    support = Support.get_support_by_user(user)
    company = support.company
    if support.is_admin:
        groups = UserGroup.objects.filter(support__company=company)
    else:
        groups = UserGroup.objects.filter(support__company=company, support=support)
    return groups

def get_group_by_id(id, user):
    company = Support.get_company_by_user(user)
    try:
        group = UserGroup.objects.get(id=id)
    except UserGroup.DoesNotExist:
        raise GroupNotFoundException()  
    if group.support.company != company:
        raise GroupNotFoundException()
    return group

def update_group(group, serializer, user):
    support = get_support_by_id(serializer.validated_data['support_id'], user)
    promo = get_promo_by_id(serializer.validated_data['promo_id'])
    if promo.company != support.company:
        raise PromoNotFoundException()
    serializer.update(group, serializer.validated_data, support, promo)

def delete_group(group):
    group.delete()