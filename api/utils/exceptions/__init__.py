# coding=utf-8


class AbstractException(Exception):
    def __init__(self):
        self.message = errors[self.__class__.__name__]

# Словарь всех ошибок
errors = {
    'InvalidCredentialsException': u"Такого логина и пароля не существует",
    'UsernameAlreadyExistException': u"Пользователь с таким именем уже существует",
    'EmailAlreadyExistException': u"Пользователь с такой почтой уже существует",
    'FamilyAlreadyExistException': u"У данного пользователя уже есть семья"
}
