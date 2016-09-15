from django.conf.urls import url, include

import supports
import company
import task
import subscription
import agent
import service
import inwork
import support
import pays
from api.controllers.web.user_group import UserGroupListView, UserGroupDetailView
from api.controllers.web.subscription_type import SubscriptionTypeListView
from api.controllers.web.promo import PromoListView
from api.controllers.web.task import TaskListView, TaskDetailView
from api.controllers.web.company import CompanyStatisticView


urlpatterns = [
	url(r'^subscription-types/$', SubscriptionTypeListView.as_view()),
    url(r'^supports/', include(supports)),
    url(r'^support/', include(support)),
    url(r'^company/', include(company)),
    url(r'^companies/', CompanyStatisticView.as_view()),
    url(r'^user-groups/$', UserGroupListView.as_view()),
    url(r'^user-groups/(?P<id>[0-9]+)/$', UserGroupDetailView.as_view()),
    url(r'^promos/$', PromoListView.as_view()),
    url(r'^agents/', include(agent)),
    url(r'^tasks/', include(task)),
    url(r'^subscriptions/', include(subscription)),
    url(r'^service/', include(service)),
    url(r'^inwork/', include(inwork)),
    url(r'^pays/', include(pays)),
]