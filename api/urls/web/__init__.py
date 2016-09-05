from django.conf.urls import url, include

import supports
import company
import task
import subscription
import agent
from api.controllers.support import SupportProfileView
from api.controllers.user_group import UserGroupListView, UserGroupDetailView
from api.controllers.subscription_type import SubscriptionTypeListView
from api.controllers.promo import PromoListView
from api.controllers.task import TaskListView, TaskDetailView
from api.controllers.agent import AgentProfileSerializer


urlpatterns = [
	url(r'^subscription-types/$', SubscriptionTypeListView.as_view()),
    url(r'^supports/', include(supports)),
    url(r'^support/$', SupportProfileView.as_view()),
    url(r'^company/', include(company)),
    url(r'^user-groups/$', UserGroupListView.as_view()),
    url(r'^user-groups/(?P<id>[0-9]+)/$', UserGroupDetailView.as_view()),
    url(r'^promos/$', PromoListView.as_view()),
    url(r'^agents/', include(agent)),
    url(r'^agent/$', AgentProfileSerializer.as_view()),
    url(r'^tasks/', include(task)),
    url(r'^subscriptions/', include(subscription))
]