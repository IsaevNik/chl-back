from django.conf.urls import url


from api.controllers.task_address import TaskForAgentView


urlpatterns = [
	url(r'^(?P<id>[0-9]+)/$', TaskForAgentView.as_view()),
]