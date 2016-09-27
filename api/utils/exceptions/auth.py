# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class InvalidCredentialsException(AbstractException):
    pass


class InvalidEmailException(AbstractException):
    pass


class InvalidLoginException(AbstractException):
	pass


class InvalidPhoneException(AbstractException):
    pass