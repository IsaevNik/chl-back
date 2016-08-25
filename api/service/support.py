# coding=utf-8
import pickle
import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from django.db import transaction

from api.utils.exceptions.user import UsernameAlreadyExistException, \
    EmailAlreadyExistException, FamilyAlreadyExistException
from api.utils.exceptions.auth import InvalidCredentialsException, \
    InvalidEmailException
from api.models.company import Company
from api.models.support import Support


def create_support_start(serializer, request_user):
    '''
    Создание экземпляра класса Support, сериализация его и запись в кеш 
    и отправка токена на фронт для создания ссылки подтверждения почты
    '''
    if User.objects.filter(username=serializer.validated_data['email']).exists():
        raise EmailAlreadyExistException
    company = (Support.get_support_by_user(request_user)).company
    support = serializer.create(serializer.validated_data, company)

    token = hashlib.sha256(support.user.email + str(datetime.now())).hexdigest()
    cache.set(token, pickle.dumps(support), 60*60*24*60)

    return token

@transaction.atomic
def create_support_finish(serializer):

    token = serializer.validated_data['token']
    password = serializer.validated_data['password']
    email = serializer.validated_data['email']

    support_ser = cache.get(token)
    support = pickle.loads(cache.get(token))
    s_user = support.user
    cache.delete(token)

    if s_user.email != email:
        raise InvalidEmailException()

    user = User.objects.create(first_name=s_user.first_name,
                               last_name=s_user.last_name,
                               username=s_user.username,
                               email=s_user.email)
    user.set_password(password)
    user.save()
    support.user = user
    
    support.save()



def auth_support(email, password):
    user = User.objects.get(email=email)
    if user.check_password(password):
        # http://stackoverflow.com/questions/20683824/how-can-i-change-existing-token-in-the-authtoken-of-django-rest-framework
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Token.objects.create(user=user).key
    raise InvalidCredentialsException()


def get_all_support():
    return Support.objects.all()