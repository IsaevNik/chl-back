# coding=utf-8
from ..utils.exceptions.task import AddressNotExistException
from api.models.task_address import TaskAddress


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

    
