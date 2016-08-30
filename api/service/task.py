# coding=utf-8

from api.models.task import Task
from api.utils.exceptions.task import TaskLimitException

def get_data_for_task(json_task, user):
    data = {}
    data['client_name'] = json_task.get('client_name', '')
    data['title'] = json_task.get('title', '')
    data['description'] = json_task.get('description', '')
    data['price'] = json_task.get('price', None)
    data['start_dt'] = json_task.get('start_dt', None)
    data['finish_dt'] = json_task.get('finish_dt', '')
    data['group_id'] = json_task.get('group_id', 0)
    data['is_start'] = json_task.get('is_start', 0)
    return data


def create_task(serializer, support, group=None):
    if support.company.task_left < 1:
        raise TaskLimitException
    if serializer.validated_data['is_start']:
        try:
            old_start_task = Task.objects.get(creater__company=support.company,
                               is_start=True)
            old_start_task.is_start = False
            old_start_task.save()
        except Task.DoesNotExist:
            pass

    task = serializer.create(serializer.validated_data, support, group)
    support.company.task_left -= 1
    support.company.save()
    return task