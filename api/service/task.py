# coding=utf-8
from django.db import transaction, connection

from api.models.task import Task
from api.models.task_address import TaskAddress
from api.models.task_filled import TaskFilled
from api.models.point_blank import PointBlank
from api.utils.exceptions.task import TaskLimitException
from base_service import get_object
from ..utils.exceptions.task import StartTaskAlreadyExist, \
    TaskNotFoundException, StartTaskNotExistException
from agent import get_agent_by_user



def get_data_for_task(json_task, user):
    data = {}
    data['client_name'] = json_task['client_name']
    data['title'] = json_task['title']
    data['description'] = json_task['description']
    data['price'] = json_task['price']
    data['start_dt'] = json_task['start_dt']
    data['finish_dt'] = json_task['finish_dt']
    data['group_id'] = json_task.get('group_id', None)
    data['is_start'] = json_task.get('is_start', 0)
    return data

def create_task(serializer, support, group):
    '''
    Функция создания задания
    '''
    #Проверка на количество оставшихся в компании заданий
    if support.company.task_left < 1:
        raise TaskLimitException
    #Если указано что задание стартовое, попробовать найти 
    if serializer.validated_data['is_start']:
        try:
            old_start_task = Task.objects.get(
                                creater__company=support.company,
                               is_start=True)
            raise StartTaskAlreadyExist()
        except Task.DoesNotExist:
            pass

    task = serializer.create(serializer.validated_data, support, group)
    support.company.task_left -= 1
    support.company.save()
    return task

def update_task(serializer, task, support, new_group):
    task = serializer.update(task, serializer.validated_data, support, new_group)
    return task


def get_task_by_id(id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise TaskNotFoundException()
    return task


def get_start_task_by_company(company):
    try:
        task = Task.objects.get(creater__company=company,
                                is_start=True)
        return task
    except Task.DoesNotExist:
        raise StartTaskNotExistException()


def get_tasks_without_address(user):
    agent = get_agent_by_user(user)
    group = agent.group
    tasks = []
    with connection.cursor() as cursor:
        #TODO datetime("NOW", "localtime") -> NOW() task.is_start=0 -> task.is_start=False
        sql = \
            'SELECT task.id, address.id FROM api_task AS task, api_taskaddress as address WHERE '\
            'task.group_id={0} AND address.task_id=task.id AND address.amount>0 AND task.start_dt<datetime("NOW", "localtime") ' \
            'AND task.finish_dt>datetime("NOW", "localtime") AND task.is_start=0 AND address.longitude IS NULL ORDER BY task.id;'
        cursor.execute(sql.format(group.id))
        for raw in cursor.fetchall():
            address_id = raw[1]
            task_address = TaskAddress.objects.get(id=address_id)
            if not TaskFilled.objects.filter(task_address=task_address, executer=agent).exists():
                tasks.append(task_address)
        return tasks

def get_tasks_with_address(data, user):
    agent = get_agent_by_user(user)
    group = agent.group

    longitude = data['longitude']
    latitude = data['latitude']

    tasks = []
    with connection.cursor() as cursor:
        # datetime("NOW", "localtime") -> NOW()
        """sql = \
            'SELECT task.id, address.id, distance(address.latitude, address.longitude, {0}, {1}) AS distance '\
            'FROM api_task AS task, api_taskaddress as address WHERE task.group_id={2} AND address.task_id=task.id '\
            'AND address.amount>0 AND task.start_dt<datetime("NOW", "localtime") AND ' \
            'task.finish_dt>datetime("NOW", "localtime") AND address.longitude IS NOT NULL ORDER BY distance;'
        cursor.execute(sql.format(latitude, longitude, group.id))"""
        sql = \
            'SELECT task.id, address.id '\
            'FROM api_task AS task, api_taskaddress as address WHERE task.group_id={0} AND address.task_id=task.id '\
            'AND address.amount>0 AND task.start_dt<datetime("NOW", "localtime") AND ' \
            'task.finish_dt>datetime("NOW", "localtime") AND task.is_start=0 AND address.longitude IS NOT NULL;'
        cursor.execute(sql.format(group.id))
        for raw in cursor.fetchall():
            address_id = raw[1]
            task_address = TaskAddress.objects.get(id=address_id)
            if not TaskFilled.objects.filter(task_address=task_address, executer=agent).exists():
                task_address.set_distance(longitude, latitude)
                tasks.append(task_address)
        return tasks


def get_point_blanks_by_task(task):
    point_blanks = PointBlank.objects.filter(task=task)
    return point_blanks