# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class SupportLimitException(AbstractException):
    pass

class AgentLimitException(AbstractException):
    pass

class SubcriptionTimeOutException(AbstractException):
	pass

class SupportNotFoundException(AbstractException):
	pass

class PromoNotFoundException(AbstractException):
	pass

class GroupNotFoundException(AbstractException):
	pass