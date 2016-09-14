from django.conf.urls import url, include

from api.controllers.web.task import TaskListView, TaskDetailView, \
    StartTaskView

urlpatterns = [
    url(r'^$', TaskListView.as_view()),
    url(r'^(?P<id>[0-9]+)/$', TaskDetailView.as_view()),
    url(r'^start/$', StartTaskView.as_view())
]