from django.conf.urls import url, include

import supports
import company
from api.controllers.support import SupportProfileView
from api.controllers.user_group import UserGroupListView, UserGroupDetailsView


urlpatterns = [
    url(r'^supports/', include(supports)),
    url(r'^support/$', SupportProfileView.as_view()),
    url(r'^company/', include(company)),
    url(r'^user-groups/$', UserGroupListView.as_view()),
    url(r'^user-group/(?P<id>[0-9]+)/$', UserGroupDetailsView.as_view())
]