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
    'SupportRoleException': u"Пользователя с данной ролью создать невозможно",
    'WithoutGroupTaskCreateException': u"Вы можете создавать задания только для определённой группы",
    'TaskLimitException': u"К сожалению вы израсходовали лимит заданий, предусмотренных вашим тарифом",
    'StartTaskWithGroupException': u"Для создания стартового задания поле 'Группа' - не заполняется",
    'StartTaskCreateException': u"Вы не можете создать вводное задание",
    'AddressNotExistException': u"Адрес и координаты должны быть заполнены",
    'StartTaskAlreadyExist': u"Вводное задание уже существует, для начала удалите его",
    'OrderNotExistException': u"Ошибка регистрации платежа",
    'SupportLimitException': u"Достигнут лимит количества операторов, предусмотренный вашим тарифом",
    'AgentLimitException': u"Достигнут лимит количества агентов, предусмотренный вашим тарифом",
    'DoesNotSelectImageException': u"Изображение не выбрано",
    'InvalidTypeOfImgException': u"Недопустимый тип файла, допустимый: *.png",
    'TaskTimeException': u"Вы не можете просматривать просроченные задания",
    'TaskAmountException': u"Данных заданий больше не осталось",
    'TaskAlreadyInWorkException': u"Вы уже выполняете это задание",
    'TaskNotDoneException': u"Агент ещё не приступил к выполнению этого задания",
    'TaskMustNotBeCheckingException': u"Задание ещё не выполнено, либо уже проверено",
    'TaskStatusException': u"Недопустимый статус для задания",
    'CancelTaskException': u"Задание недоступно для удаления",
    'DoTaskException': u"Задание недоступно для выполнения"
}
