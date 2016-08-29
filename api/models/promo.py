# coding: utf-8
from django.db import models

from company import Company


class Promo(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    img_url = models.CharField(max_length=100)
    limit = models.IntegerField(default=0)
    company = models.ForeignKey(Company, 
    							related_name='promos', 
    							on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title