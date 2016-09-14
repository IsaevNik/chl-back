# coding=utf-8
from django.utils import timezone

from ..utils.exceptions.task import AddressNotExistException, TaskTimeException, \
    TaskAmountException, TaskAlreadyInWorkException
from api.models.task_address import TaskAddress
from api.models.task_filled import TaskFilled
from base_service import get_object

def create_task_address(serializer, task, support):
    data = serializer.validated_data
    if (data['longitude'] and data['latitude'] and data['address']) or \
       not (data['longitude'] or data['latitude'] or data['address']):
        serializer.create(serializer.data, task)
    else:
        raise AddressNotExistException


def update_task_address(serializer, task, ids):
    id = serializer.validated_data['id']
    if not id:
        # если адреса не было в предыдущей версии задания - создать
        serializer.create(serializer.data, task)
    elif id in ids:
        # если было в предыдущей версии задания и остался в изменённой - изменить
        task_address = TaskAddress.objects.get(id=id)
        serializer.update(task_address, serializer.validated_data)
    else:
        pass


def delete_task_addresses(ids):
    deleted_task_addresses = TaskAddress.objects.exclude(id__in=ids)
    for task_address in deleted_task_addresses:
        task_address.delete()

    
def get_task_address(id):
    task = get_object(TaskAddress, id)
    return task

def is_task_available(task_address):
    task = task_address.task
    if timezone.now() > task.finish_dt:
        raise TaskTimeException()
    if task_address.amount < 1:
        raise TaskAmountException()


def taken_task_by_agent(task_address, agent):
    task = task_address.task
    
    if TaskFilled.objects.filter(task_address=task_address, executer=agent).exists():
        raise TaskAlreadyInWorkException()
    
    task_filled = TaskFilled(
        task_address=task_address,
        executer=agent)
    if not task.is_start:
        task_address.amount -= 1
        task_address.save()
    task_filled.save()
