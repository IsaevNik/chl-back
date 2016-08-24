# coding=utf-8
import pickle

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from django.db import transaction

from api.utils.exceptions.user import EmailAlreadyExistException
from api.models.company import Company
from api.models.support import Support

@transaction.atomic
def create_support_start(serializer, request_user):
    '''
    Создание экземпляра класса Support, сериализация его и запись в кеш 
    и отправка токена на фронт для создания ссылки подтверждения почты
    '''
    if User.objects.filter(username=serializer.validated_data['email']).exists():
        raise EmailAlreadyExistException
    company = (Support.get_support_by_user(request_user)).company
    support = serializer.create(serializer.validated_data, company)
    token = Token(user=support.user)
    token.save()
    #cache.set(token, pickle.dumps(support), 60*60*24*60)

    return token.key
