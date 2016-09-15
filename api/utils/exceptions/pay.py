# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class OrderNotExistException(AbstractException):
    pass


class LowBalanceException(AbstractException):
	pass


class PayStatusException(AbstractException):
	pass


class PayAlreadyCheckException(AbstractException):
	pass