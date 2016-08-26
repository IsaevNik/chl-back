# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class AdminDeleteException(AbstractException):
    pass

class ChangeAdminToSupportException(AbstractException):
	pass