# coding: utf-8

from django.db import models

from support import Support
#from promo import Promo


class UserGroup(models.Model):
    name = models.CharField(max_length=64)
    support = models.ForeignKey(Support, related_name='groups')
#    promos = models.ForeignKey(Promo, related_name='groups') 

    def __unicode__(self):
        return self.name