# coding: utf-8

from django.db import models

from agent import Agent
from pay import Pay


class Purse(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, related_name='purse')
    balance = models.IntegerField(default=0) 

    def __unicode__(self):
        return self.agent.name

    # метод отражающий баланс агента с учётом запрошенных поощрений
    def get_balance(self):
    	pays = Pay.objects.filter(status=0, agent=self.agent)
    	pays_requset_sum = sum([pay.agent.group.promos.limit for pay in pays])
    	return self.balance - pays_requset_sum


