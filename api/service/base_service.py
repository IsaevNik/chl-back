# coding=utf-8
from rest_framework.exceptions import NotFound


def get_all(mdl):
    return mdl.objects.all()


def get_object(mdl, pk):
    try:
        return mdl.objects.get(id=pk)
    except mdl.DoesNotExist:
        raise NotFound()


