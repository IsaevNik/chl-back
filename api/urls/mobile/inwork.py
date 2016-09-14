from django.conf.urls import url


from api.controllers.mobile.inwork import InWorkTaskDetailView, BlanksOfTaskView, \
    InWorkTasksListView, InWorkAgentsTaskListView, InWorkAgentsHistoryListView


urlpatterns = [
	url(r'^$', InWorkAgentsTaskListView.as_view()),
	url(r'^history/$', InWorkAgentsHistoryListView.as_view()),
    url(r'^(?P<id>[0-9]+)/$', InWorkTaskDetailView.as_view()),
    url(r'^(?P<id>[0-9]+)/blanks/$', BlanksOfTaskView.as_view()),
    url(r'^by-status/(?P<status>[0-4])/$', InWorkTasksListView.as_view()),
]