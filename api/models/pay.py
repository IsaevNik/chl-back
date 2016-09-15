# coding: utf-8

from django.db import models

from agent import Agent


class Pay(models.Model):
    REQUEST = 0
    SUCCESS = 1
    FAIL = 2
    STATUS_CHOICES = (
        (REQUEST, 'Запрошено'),
        (SUCCESS, 'Одобрено'),
        (FAIL, 'Отказано')
    )
    request_dt = models.DateTimeField(auto_now_add=True)
    check_dt = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="pays")
    status = models.IntegerField(choices=STATUS_CHOICES, default=REQUEST)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)
