# coding: utf-8

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from company import Company
from user_group import UserGroup


class Agent(models.Model):
    ANDROID = 1
    IOS = 2
    OS_CHOICES = (
        (ANDROID, 'Android'),
        (IOS, 'IOS')
    )
    phone = models.CharField(max_length=11)
    platform = models.IntegerField(choices=OS_CHOICES, blank=True, null=True)
    device_id = models.CharField(max_length=1000, blank=True)
    company = models.ForeignKey(Company, 
                                related_name='agents', 
                                on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, related_name='agents')
    post = models.CharField(max_length=32, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def name(self):
        return self.user.first_name + " " + self.user.last_name

    @staticmethod
    def get_agent_by_user(user):
        return Agent.objects.get(user=user)
    