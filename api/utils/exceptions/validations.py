# coding=utf-8

from api.utils.exceptions import AbstractException


class InvalidProfileTypeException(AbstractException):
    def __init__(self, value):
        super(AbstractException, self).__init__("{0} нет среди типов профелей. Активные типы: ".format(value),)
