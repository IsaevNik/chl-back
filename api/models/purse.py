# coding: utf-8

from django.db import models

from agent import Agent


class Purse(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, related_name='purse')
    balance = models.IntegerField(default=0) 

    def __unicode__(self):
        return self.agent.name