# coding=utf-8
from api.utils.exceptions import AbstractException


class RequestValidationException(AbstractException):
    """
    В конструктор данного исключения передается сериалайзер,
    дабы добавить сообщения об ошибках валидации запроса.
    """
    def __init__(self, serializer):
        self.message = serializer.errors
