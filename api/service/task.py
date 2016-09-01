# coding=utf-8
from django.db import transaction

from api.models.task import Task
from api.models.task_address import TaskAddress
from api.models.point_blank import PointBlank
from api.utils.exceptions.task import TaskLimitException
from base_service import get_object
from ..utils.exceptions.task import StartTaskAlreadyExist


def get_data_for_task(json_task, user):
    data = {}
    data['client_name'] = json_task['client_name']
    data['title'] = json_task['title']
    data['description'] = json_task['description']
    data['price'] = json_task['price']
    data['start_dt'] = json_task['start_dt']
    data['finish_dt'] = json_task['finish_dt']
    data['group_id'] = json_task.get('group_id', 0)
    data['is_start'] = json_task.get('is_start', 0)
    return data

@transaction.atomic
def create_task(serializer, support, group):
    '''
    Функция создания задания
    '''
    #Проверка на количество оставшихся в компании заданий
    if support.company.task_left < 1:
        raise TaskLimitException
    #Если указано что задание стартовое, попробовать найти 
    #стартовое задание на текущий момент и снять у него флаг is_start
    if serializer.validated_data['is_start']:
        try:
            old_start_task = Task.objects.get(
                                creater__company=support.company,
                               is_start=True)
            raise StartTaskAlreadyExist
        except Task.DoesNotExist:
            pass

    task = serializer.create(serializer.validated_data, support, group)
    support.company.task_left -= 1
    support.company.save()
    return task

def update_task(serializer, task, support, new_group):
    task = serializer.update(task, serializer.validated_data, support, new_group)
    return task




@transaction.atomic
def reset_task(task, support):
    #удаляем задание и возвращаем значение оставшихся заданий    
    task.delete()
    support.company.task_left += 1
    support.company.save()


def get_task(id):
    task = get_object(Task, id)
    return task