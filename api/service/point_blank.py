# coding=utf-8
import json

from task import reset_task
from api.models.point_blank import PointBlank

def create_blank(serializer, task):
    data = serializer.validated_data
    if data['type'] == 2:
        data['content'] = json.dumps(data['content'])
    else:
        data['content'] = data['content']['text']
    serializer.create(data, task)


def update_blank(serializer, task, ids):
    id = serializer.validated_data['id']
    data = serializer.validated_data
    # если бланка не было в предыдущей версии задания - создать
    if not id:
        create_blank(serializer, task)
    # если был в предыдущей версии задания и остался в изменённой - изменить
    elif id in ids:
        blank = PointBlank.objects.get(id=id)
        if data['type'] == 2:
            data['content'] = json.dumps(data['content']) 
        else:
            data['content'] = data['content']['text']

        serializer.update(blank, data)
    else:
        pass

def delete_blanks(ids):
    deleted_blanks = PointBlank.objects.exclude(id__in=ids)
    for blank in deleted_blanks:
        blank.delete()