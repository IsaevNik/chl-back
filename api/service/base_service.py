# coding=utf-8
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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


def auth_user(login, password):
    user = User.objects.get(username=login)
    if user.check_password(password):
        # http://stackoverflow.com/questions/20683824/how-can-i-change-existing-token-in-the-authtoken-of-django-rest-framework
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Token.objects.create(user=user).key
    raise InvalidCredentialsException()