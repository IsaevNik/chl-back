# coding: utf-8
from django.db import models

from task import Task


class TaskAddress(models.Model):
    task = models.ForeignKey(Task, related_name="task_addresses", on_delete=models.CASCADE)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    amount = models.IntegerField()

    def __unicode__(self):
        return str(self.id)
