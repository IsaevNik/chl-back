from django.conf.urls import url


from api.controllers.agent import AgentProfileView, LogoutAgentView, LoginAgentView


urlpatterns = [
	url(r'^$', AgentProfileView.as_view()),
	url(r'^logout/$', LogoutAgentView.as_view()),
    url(r'^login/$', LoginAgentView.as_view())

]