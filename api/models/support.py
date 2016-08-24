# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from company import Company


class Support(models.Model):
    ADMIN = 1
    OPERATOR = 2
    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (OPERATOR, 'Оператор')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, 
                                related_name="supports",
                                on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES, default=OPERATOR)
    post = models.CharField(max_length=100, blank=True)


    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def name(self):
        return self.user.first_name + " " + self.user.last_name
    

    @property
    def is_admin(self):
        if self.role == 1:
            return True
        return False
    
    @staticmethod
    def get_support_by_user(user):
        return Support.objects.get(user=user)