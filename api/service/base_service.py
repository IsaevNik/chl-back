# coding=utf-8
from datetime import datetime
import os
import imghdr
from random import randrange

from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings

from api.models.support import Support
from api.models.agent import Agent
from ..utils.exceptions.task import InvalidTypeOfImgException
from ..utils.exceptions.auth import InvalidCredentialsException


def get_all(mdl):
    return mdl.objects.all()


def get_object(mdl, pk):
    try:
        return mdl.objects.get(id=pk)
    except mdl.DoesNotExist:
        raise NotFound()


def logout_user(user):
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return None
    token.delete()


def is_support(user):
    try:
        support = Support.get_support_by_user(user)
    except Support.DoesNotExist:
        return False
    return True



def auth_user(login, password):
    try:
        user = User.objects.get(username=login)
    except User.DoesNotExist:
        raise InvalidCredentialsException()
    if user.check_password(password):
        # http://stackoverflow.com/questions/20683824/how-can-i-change-existing-token-in-the-authtoken-of-django-rest-framework
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Token.objects.create(user=user).key
    raise InvalidCredentialsException()


def get_company_by_user(user):
    try:
        support = Support.objects.get(user=user)
        company = support.company
        return company
    except Support.DoesNotExist:
        try:
            agent = Agent.objects.get(user=user)
            company = agent.company
            return company
        except Agent.DoesNotExist:
            raise NotFound()
            

def save_image(img_file, user):
    company = get_company_by_user(user)
    company_id = company.id

    if imghdr.what(img_file) == 'png':
        today = datetime.now()
        photo_name = str(today.strftime('%d%m%Y')) + '_' + str(randrange(1, 9999)) + '.png'
        destination_dir = os.path.join(settings.MEDIA_ROOT,'expl', str(company_id))

        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)

        expl_image = os.path.join(destination_dir, photo_name)
        img_url = settings.MEDIA_URL + '/'.join(['expl', str(company_id), photo_name])

        with open(expl_image, 'wb+') as destination:
            for chunk in img_file.chunks():
                destination.write(chunk)

        return img_url
    else:
        raise InvalidTypeOfImgException


def get_user_by_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        raise NotFound()
    return token.user