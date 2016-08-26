# coding: utf-8 

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64)
    contact_person_first_name = models.CharField(max_length=64)
    contact_person_last_name = models.CharField(max_length=64)
    contact_person_phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255)
    #TODO default logo url
    logo_img = models.CharField(max_length=100)
    screen = models.TextField(blank=True)
    invite_text = models.TextField(blank=True)
    checking_acc =  models.CharField(blank=True, max_length=12)
    bank_name = models.CharField(blank=True, max_length=255)
    ogrn = models.CharField(blank=True, max_length=20)
    inn = models.CharField(blank=True, max_length=12)
    kpp = models.CharField(blank=True, max_length=12)
    ur_address = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    task_left = models.IntegerField(default=5)


    def __unicode__(self):
        return self.name

    @property
    def supports_left(self):
        pass

    @property
    def agents_left(self):
        pass

    @property
    def time_to_finish_subscription(self):
        pass
    
    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs) 
        return self
        