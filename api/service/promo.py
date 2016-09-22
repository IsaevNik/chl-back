# coding=utf-8
from rest_framework.exceptions import NotFound

from api.models.support import Support
from api.models.promo import Promo
from support import get_support_by_user
from base_service import get_object
from api.utils.exceptions.company import PromoNotFoundException


def create_promo(serializer, user):
    support = get_support_by_user(user)
    serializer.create(serializer.validated_data, support.company)


def get_all_promo_of_company(user):
    company=Support.get_company_by_user(user)
    return Promo.objects.filter(company=company)


def get_promo_by_id(id):
    try:
        promo = Promo.objects.get(id=id)
    except Promo.DoesNotExist:
        raise PromoNotFoundException()
    return promo


def delete_promo(promo):
    promo.delete()

