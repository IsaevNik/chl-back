from django.conf.urls import url


from api.controllers.mobile.task import TaskForAgentView


urlpatterns = [
	url(r'^(?P<id>[0-9]+)/$', TaskForAgentView.as_view()),
]