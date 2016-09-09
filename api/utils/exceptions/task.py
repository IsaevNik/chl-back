# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class WithoutGroupTaskCreateException(AbstractException):
    pass

class TaskLimitException(AbstractException):
    pass

class StartTaskWithGroupException(AbstractException):
    pass

class StartTaskCreateException(AbstractException):
    pass

class AddressNotExistException(AbstractException):
    pass

class StartTaskAlreadyExist(AbstractException):
    pass

class DoesNotSelectImageException(AbstractException):
	pass

class InvalidTypeOfImgException(AbstractException):
	pass