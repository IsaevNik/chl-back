from django.conf.urls import url


from api.controllers.mobile.agent import AgentProfileView, LogoutAgentView, LoginAgentView, \
    RecoverPasswordStartView, RecoverPasswordFinishView

urlpatterns = [
    url(r'^$', AgentProfileView.as_view()),
    url(r'^logout/$', LogoutAgentView.as_view()),
    url(r'^login/$', LoginAgentView.as_view()),
    url(r'^recover-password-start/$', RecoverPasswordStartView.as_view()),
    url(r'^recover-password-finish/$', RecoverPasswordFinishView.as_view()),

]