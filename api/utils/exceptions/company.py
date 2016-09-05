# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class SupportLimitException(AbstractException):
    pass

class AgentLimitException(AbstractException):
    pass