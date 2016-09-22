# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class SupportRoleException(AbstractException):
    pass

class InvalidTokenException(AbstractException):
	pass