from django.conf.urls import url, include

import supports
import company
from api.controllers.support import SupportProfileView
from api.controllers.user_group import UserGroupListView, UserGroupDetailView
from api.controllers.subscription_type import SubscriptionTypeListView
from api.controllers.agent import AgentListView, AgentDetailView
from api.controllers.promo import PromoListView
from api.controllers.task import TaskListView


urlpatterns = [
	url(r'^subscription-types/$', SubscriptionTypeListView.as_view()),
    url(r'^supports/', include(supports)),
    url(r'^support/$', SupportProfileView.as_view()),
    url(r'^company/', include(company)),
    url(r'^user-groups/$', UserGroupListView.as_view()),
    url(r'^user-groups/(?P<id>[0-9]+)/$', UserGroupDetailView.as_view()),
    url(r'^promos/$', PromoListView.as_view()),
    url(r'^agents/$', AgentListView.as_view()),
    url(r'^agents/(?P<id>[0-9]+)/$', AgentDetailView.as_view()),
    url(r'^tasks/$', TaskListView.as_view())
]