from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#from django.db import transaction

#from api.controllers.serializers.user import FamilySerializer
from api.models.support import Support
from api.utils.exceptions.auth import InvalidCredentialsException
from api.utils.exceptions.user import UsernameAlreadyExistException, EmailAlreadyExistException, \
    FamilyAlreadyExistException


def auth(email, password):
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
