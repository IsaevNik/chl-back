# coding=utf-8
from api.utils.exceptions import AbstractException
from . import errors


class TaskNotDoneException(AbstractException):
    pass


class TaskMustNotBeCheckingException(AbstractException):
	pass


class TaskStatusException(AbstractException):
	pass


class CancelTaskException(AbstractException):
	pass


class DoTaskException(AbstractException):
	pass


class TaskFilledNotFoundException(AbstractException):
	pass