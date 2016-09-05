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
    task_left = models.IntegerField(blank=True)


    def __unicode__(self):
        return self.name


    def _get_active_subscription(self):
        subscriptions = filter(lambda sub: sub.start_dt, self.subscriptions.all())
        all_subscriptions = sorted(subscriptions, 
                                   key=lambda sub: sub.start_dt,
                                   reverse=True)
        active_subscription = filter(lambda sub: sub.status == 2, all_subscriptions)[0]
        return active_subscription


    @property
    def active_subscription(self):
        return self._get_active_subscription
    

    @property
    def supports_left(self):
        support_limit = self._get_active_subscription().subscription_type.support_limit
        now_supports_sum = self.supports_now

        return support_limit - now_supports_sum


    @property
    def agents_left(self):
        agent_limit = self._get_active_subscription().subscription_type.user_limit
        now_agents_sum = self.active_agents

        return agent_limit - now_agents_sum


    @property
    def time_to_finish_subscription(self):
        active_subscription = self._get_active_subscription()
        return active_subscription.end_dt
    

    @property
    def supports_now(self):
        return len(self.supports.all())


    @property
    def invited_agents(self):
        return len(self.agents.all())


    @property
    def active_agents(self):
        return len(filter(lambda agent: agent.platform, self.agents.all()))


    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs) 
        return self


    