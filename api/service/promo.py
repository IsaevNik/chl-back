# coding=utf-8
from rest_framework.exceptions import NotFound

from api.models.support import Support
from api.models.promo import Promo
from support import get_support, get_support_by_user
from base_service import get_object


def create_promo(serializer, user):
    support = get_support_by_user(user)
    company = support.company

    Promo.objects.create(title=serializer.validated_data['title'],
                  description=serializer.validated_data.get('description', ''),
                  img_url=serializer.validated_data['img_url'],
                  limit=serializer.validated_data['limit'],
                  company=company)


def get_all_promo_of_company(user):
    company=Support.get_company_by_user(user)
    return Promo.objects.filter(company=company)


def get_promo(promo_id):
    try:
        promo = Promo.objects.get(id=promo_id)
    except UserGroup.DoesNotExist:
        raise NotFound
    return promo


'''def get_all_groups_of_company(user):
    support = Support.get_support_by_user(user)
    company = support.company
    if support.is_admin:
        groups = UserGroup.objects.filter(support__company=company)
    else:
        groups = UserGroup.objects.filter(support__company=company, support=support)
    return groups

def get_group(id, user):
    company = Support.get_company_by_user(user)
    group = get_object(UserGroup, id)
    if group.support.company != company:
        raise NotFound()
    return group

def update_group(group, serializer, user):
    support = get_support(serializer.validated_data['support_id'], user)
    group.support = support
    group.name = serializer.validated_data['name']
    group.save()

def delete_group(group):
    group.delete()'''