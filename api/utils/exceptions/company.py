# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class SupportNotFoundException(AbstractException):
    pass

class PromoNotFoundException(AbstractException):
    pass

class GroupNotFoundException(AbstractException):
    pass

class CompanyNotFoundException(AbstractException):
    pass

class AgentNotFoundException(AbstractException):
    pass

