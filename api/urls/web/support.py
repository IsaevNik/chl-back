from django.conf.urls import url


from api.controllers.web.support import LoginSupportView, SupportProfileView, \
	LogoutSupportView, RecoverPasswordStartView, RecoverPasswordFinishView


urlpatterns = [
	url(r'^$', SupportProfileView.as_view()),
    url(r'^login/$', LoginSupportView.as_view()),
    url(r'^logout/$', LogoutSupportView.as_view()),
    url(r'^recover-password-start/$', RecoverPasswordStartView.as_view()),
    url(r'^recover-password-finish/$', RecoverPasswordFinishView.as_view()),
]