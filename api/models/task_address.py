# coding: utf-8
import math

from django.db import models

from task import Task


class TaskAddress(models.Model):
    
    task = models.ForeignKey(Task, related_name="task_addresses", on_delete=models.CASCADE)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    amount = models.IntegerField()

    _distance = 0.0

    def __unicode__(self):
        return str(self.id)

    @property
    def distance(self):
        return self._distance

    def set_distance(self,longitude, latitude):
        dist = math.hypot(longitude-self.longitude,
            latitude-self.latitude)
        self._distance = dist
    
    