# coding: utf-8
from django.db import models
from django.utils import timezone

from agent import Agent
from support import Support
from task_address import TaskAddress


class TaskFilled(models.Model):
    TAKEN = 0
    DONE = 1
    REFUSED = 2
    ACCEPT = 3
    FAIL = 4
    STATUS_CHOICES = (
        (TAKEN, 'Взято на выполнение'),
        (DONE, 'Выполнено'),
        (REFUSED, 'Отказ от выполнения'),
        (ACCEPT, 'Одобрено'),
        (FAIL, 'Не принято'),
    )
    task_address = models.ForeignKey(TaskAddress)
    executer = models.ForeignKey(Agent, related_name="execute_tasks")
    checker = models.ForeignKey(Support, related_name="check_tasks", blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TAKEN)
    take_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField(blank=True, null=True)
    check_dt = models.DateTimeField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
