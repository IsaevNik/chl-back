# coding=utf-8
from django.contrib import admin

from .models.support import Support
from .models.company import Company 
from .models.user_group import UserGroup 
from .models.subscription_type import SubscriptionType
from .models.agent import Agent
from .models.promo import Promo
from .models.task import Task
from .models.task_address import TaskAddress
from .models.point_blank import PointBlank
#from .models.subscription import Subscription


'''class SubscriptionAdmin(admin.ModelAdmin):

    def company_name(self, obj):
        return obj.company

    def when_end(self, obj):
        return obj.when_end

    def how_much_to_end(self, obj):
        return obj.how_much_to_end

    def subscription_type_name(self, obj):
        return obj.subscription_type

    when_end.short_description = "Когда заканчивается подписка"
    how_much_to_end.short_description = "Осталось дней до оканчания"
    company_name.short_description = "Название компании"
    subscription_type_name.short_description = "Тип подписки"

    ordering = ('-purchase_dt',)

    list_display = ('company_name', 'subscription_type_name', 'how_much_to_end', 'when_end')'''


class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('title','task_limit','support_limit','user_limit','price','time')
    list_editable = ['task_limit','support_limit','user_limit','price','time']

admin.site.register(Company)
admin.site.register(Support)
admin.site.register(UserGroup)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(Agent)
admin.site.register(Promo)
admin.site.register(Task)
admin.site.register(TaskAddress)
admin.site.register(PointBlank)
