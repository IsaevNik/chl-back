# coding: utf-8

from datetime import datetime
from datetime import timedelta

from django.db import models
from django.utils import timezone

from company import Company
from subscription_type import SubscriptionType


class Subscription(models.Model):
    IN_PROGRESS = 1
    CONFIRMED = 2
    DISCARDED = 3
    LATE = 4
    TYPE_CHOICES = (
        (IN_PROGRESS, 'Проверяется'),
        (CONFIRMED, 'Подтвержден'),
        (DISCARDED, 'Отклонен'),
        (LATE, 'Просрочен')
    )


    company = models.ForeignKey('Company', related_name="subscriptions")
    purchase_dt = models.DateTimeField(auto_now_add=True)
    start_dt = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=TYPE_CHOICES)
    subscription_type = models.ForeignKey('SubscriptionType')

    class Meta:
        ordering = ('-purchase_dt',)


    @property
    def end_dt(self):
        if self.status in [2,4]:
            return self.start_dt + timedelta(days=self.subscription_type.time)
        else:
            return None

    '''@property
    def how_much_to_end(self):
        today = datetime.now()
        end_date = self.end_dt
        return (end_date - today).days'''


    def __unicode__(self):
        return str(self.id)