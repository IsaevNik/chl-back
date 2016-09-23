# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class SubscriptionTypeNotFoundException(AbstractException):
	pass

class SupportLimitException(AbstractException):
    pass

class AgentLimitException(AbstractException):
    pass

class SubcriptionTimeOutException(AbstractException):
    pass

class SubscriptionStatusException(AbstractException):
	pass

class SubscriptionNotFoundException(AbstractException):
	pass