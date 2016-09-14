# coding: utf-8

from django.db import models

from point_blank import PointBlank
from task_filled import TaskFilled


class PointFilled(models.Model):
    blank = models.ForeignKey(PointBlank, related_name='filled_points')
    task_filled = models.ForeignKey(TaskFilled, on_delete=models.CASCADE, related_name='filled_blanks')
    content = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)
