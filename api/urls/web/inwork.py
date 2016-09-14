from django.conf.urls import url, include

from api.controllers.web.inwork import InWorkTasksListView, InWorkStatsView, \
	InWorkTaskDetailView, InWorkHistoryView

urlpatterns = [
    url(r'^by-status/(?P<status>[0-4])/$', InWorkTasksListView.as_view()),
    url(r'^statistic/$', InWorkStatsView.as_view()),
    url(r'^(?P<id>[0-9]+)/$', InWorkTaskDetailView.as_view()),
    url(r'^history/$', InWorkHistoryView.as_view())

]