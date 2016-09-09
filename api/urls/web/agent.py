from django.conf.urls import url


from api.controllers.agent import AgentListView, AgentDetailView


urlpatterns = [
	url(r'^$', AgentListView.as_view()),
	url(r'^(?P<id>[0-9]+)/$', AgentDetailView.as_view()),

]