# coding: utf-8

from django.db import models

class SubscriptionType(models.Model):
    title = models.CharField("Название", max_length=64)
    description = models.TextField("Описание", blank=True)
    task_limit = models.IntegerField("Лимит кол-ва заданий", default=0)
    support_limit = models.IntegerField("Лимит кол-ва операторов", default=0)
    user_limit = models.IntegerField("Лимит кол-ва агентов",default=0)
    price = models.IntegerField("Стоимость",default=0)
    time = models.IntegerField("Срок действия подписки",default=90)

    def __unicode__(self):
        return self.title