# coding=utf-8


class AbstractException(Exception):
    def __init__(self):
        self.message = errors[self.__class__.__name__]

# Словарь всех ошибок
errors = {
    'InvalidCredentialsException': u"Такого логина и пароля не существует",
    'UsernameAlreadyExistException': u"Пользователь с таким именем уже существует",
    'EmailAlreadyExistException': u"Пользователь с такой почтой уже существует",
    'FamilyAlreadyExistException': u"У данного пользователя уже есть семья",
    'InvalidEmailException': u"Проверьте правильность введённого логина",
    'AdminDeleteException': u"Нельзя удалить администратора",
    'ChangeAdminToSupportException': u"Вы не можете поменять свою роль на 'Оператор'",
    'LoginAlredyExistException': u"Пользователь с таким логином уже существует",
}
