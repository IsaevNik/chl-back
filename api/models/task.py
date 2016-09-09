# coding: utf-8

from django.db import models
from django.utils import timezone

from support import Support
from user_group import UserGroup


class Task(models.Model):
    client_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    creater = models.ForeignKey(Support, related_name="tasks_creating")
    last_editor = models.ForeignKey(Support, related_name="taks_editing")
    group = models.ForeignKey(UserGroup, related_name="tasks", blank=True, null=True)
    price = models.IntegerField()
    start_dt = models.DateTimeField()
    finish_dt = models.DateTimeField()
    release_dt = models.DateTimeField(blank=True, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    last_edit_dt = models.DateTimeField(auto_now=True)
    execute_t = models.IntegerField(default=14400)
    is_start = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    @property
    def task_adresses_count(self):
        return len(self.task_addresses.all())