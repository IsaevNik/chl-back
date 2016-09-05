# coding=utf-8
import pickle
import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import transaction
from rest_framework.exceptions import NotFound

from api.utils.exceptions.user import UsernameAlreadyExistException, \
    EmailAlreadyExistException, FamilyAlreadyExistException
from api.utils.exceptions.auth import InvalidCredentialsException, \
    InvalidEmailException
from api.utils.exceptions.registration import SupportRoleException
from api.utils.exceptions.company import SupportLimitException
from api.utils.exceptions.admin import AdminDeleteException
from base_service import get_all, get_object
from api.models.company import Company
from api.models.support import Support
from api.models.subscription_type import SubscriptionType
from api.models.subscription import Subscription
from api.models.user_group import UserGroup


def create_support_start(serializer, request_user):
    '''
    Создание экземпляра класса Support, сериализация его и запись в кеш 
    и отправка токена на фронт для создания ссылки подтверждения почты
    '''

    if User.objects.filter(username=serializer.validated_data['email']).exists():
        raise EmailAlreadyExistException
    
    company = (Support.get_support_by_user(request_user)).company
    if company.supports_left < 1:
        raise SupportLimitException

    if serializer.validated_data['role'] in [1,3,4]:
        raise SupportRoleException

    
    support = serializer.create(serializer.validated_data, company)

    token = hashlib.sha256(support.user.email + str(datetime.now())).hexdigest()
    cache.set(token, pickle.dumps(support), 60*60*24)

    return token


def create_support_finish(serializer, is_admin=False):
    '''
    Окончание создания оператора, если функция выполняется в контексте 
    регистрации компании, то is_admin=True
    '''
    token = serializer.validated_data['token']
    password = serializer.validated_data['password']
    email = serializer.validated_data['email']

    support_ser = cache.get(token)
    support = pickle.loads(cache.get(token))

    if support.user.email != email:
        raise InvalidEmailException

    cache.delete(token)

    if is_admin:
        start_sub_type = SubscriptionType.objects.get(price=0)
        support.company.task_left = start_sub_type.task_limit
        company = support.company.save()
        support.company = company
        Subscription.objects.create(
            company=company,
            start_dt=datetime.now(),
            status=2,
            subscription_type=start_sub_type
        )


    support.user.save()
    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    support.user = user
    support.save()


def update_support(support, serializer):
    old_email = support.user.email
    new_email = serializer.validated_data['email']
    if (old_email != new_email) and (User.objects.filter(username=new_email).exists()):
        raise EmailAlreadyExistException
    support = serializer.update(support, serializer.validated_data)


def delete_support(support):
    if support.is_admin:
        raise AdminDeleteException
    user = support.user
    user.delete()


def get_all_supports_of_company(user):
    company = Support.get_company_by_user(user)
    return Support.objects.filter(company=company)


def get_support(id, user):
    company = Support.get_company_by_user(user)
    support = get_object(Support, id)
    if support.company != company:
        raise NotFound()
    return support


def get_support_by_user(user):
    try:
        support = Support.get_support_by_user(user)
    except Agent.DoesNotExist:
        raise NotFound()
    return support


def is_support(user):
    try:
        support = Support.objects.get(user=user)
    except Support.DoesNotExist:
        return False   
    return True


def get_all_groups_of_support(support):
    company = support.company
    if support.is_admin:
        return UserGroup.objects.filter(support__company=company)
    else:
        return UserGroup.objects.filter(support=support)


