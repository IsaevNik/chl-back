# coding=utf-8
import json
from datetime import datetime

from django.utils import timezone

from api.models.task_filled import TaskFilled
from api.models.point_blank import PointBlank
from api.models.support import Support
from api.models.agent import Agent
from base_service import get_object, save_image, is_support
from api.controllers.serializers.point_filled import PointFilledCreateSerializer
from api.forms import UploadFileForm
from ..utils.exceptions.commons import RequestValidationException
from ..utils.exceptions.inwork import TaskStatusException, TaskFilledNotFoundException


def get_task_inwork_by_status(status, user):
    if isinstance(user, Support):
        support = user
        if support.is_admin:
            inworks = TaskFilled.objects.filter(status=status, 
                                                executer__company=support.company)
        else:
            groups = support.groups
            inworks = TaskFilled.objects.filter(status=status,
                                                executer__group__in=groups.all())
    elif isinstance(user, Agent):
        agent=user
        inworks = TaskFilled.objects.filter(status=status, executer=agent)

    if status == 0 or status == 2:
        return inworks.order_by('take_dt')
    if status == 1:
        return inworks.order_by('end_dt')
    if status == 3 or status == 4:
        return inworks.order_by('-check_dt')

    return inworks


def get_stat_inwork(support):
    data_stat = {}
    for status in TaskFilled.STATUS_CHOICES:
        data_stat[status[1]] = len(get_task_inwork_by_status(status[0], support))
    return data_stat
    

def get_task_filled_by_id(id):
    try:
        task_filled = TaskFilled.objects.get(id=id)
    except TaskFilled.DoesNotExist:
        raise TaskFilledNotFoundException()
    return task_filled


def do_the_task(request, task_filled, serializer):

    json_task = json.loads(serializer.validated_data['task'])
    serializer.update(task_filled, serializer.validated_data)
    for point in json_task['points']:
        point_blank = get_object(PointBlank, point['id'])
        c_serializer = PointFilledCreateSerializer(data=point)
        if c_serializer.is_valid():
            data_for_create = {}
            if point_blank.type == 1:
                data_for_create['content'] = c_serializer.validated_data['content']
            elif point_blank.type == 2:
                data_for_create['content'] = json.dumps(
                                        c_serializer.validated_data['content'])
            elif point_blank.type == 3:

                data_for_create['content'] = save_image(
                                        request.FILES[c_serializer.validated_data['content']],
                                        request.user)
            c_serializer.create(data_for_create, task_filled, point_blank)
        else:
            raise RequestValidationException(c_serializer)


def cancel_the_task(task_filled):
    task_address = task_filled.task_address
    task = task_address.task
    if not task.is_start:
        task_address.amount += 1
        task_address.save()
    task_filled.delete()


def check_task(task_filled, serializer, user):
    support = Support.get_support_by_user(user)
    status = serializer.validated_data['status']
    if not status in [3, 4]:
        raise TaskStatusException() 
    if status == 3:
        task_filled.status = 3
        task_filled.checker = support
        task_filled.check_dt = timezone.now()
        task_filled.executer.purse.balance += serializer.validated_data['points']
        task_filled.save()
        task_filled.executer.purse.save()
    else:
        task_filled.status = 4
        task_filled.checker = support
        task_filled.check_dt = timezone.now()
        task_filled.comment = serializer.validated_data['comment']
        task_filled.task_address.amount += 1
        task_filled.task_address.save()
        task_filled.save()  
    


def get_task_inwork_by_user(agent, data):
    inworks_taken = get_task_inwork_by_status(0, agent)
    inworks_done = get_task_inwork_by_status(1, agent)
    inworks = (inworks_taken | inworks_done).order_by('take_dt')

    for inwork in inworks:
        if inwork.task_address.latitude:
            inwork.task_address.set_distance(data['longitude'], data['latitude'])
    return inworks
        