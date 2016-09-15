from django.conf.urls import url


from api.controllers.web.support import LoginSupportView, SupportProfileView, \
	LogoutSupportView


urlpatterns = [
	url(r'^$', SupportProfileView.as_view()),
    url(r'^login/$', LoginSupportView.as_view()),
    url(r'^logout/$', LogoutSupportView.as_view()),
]