from django.conf.urls import url


from api.controllers.web.support import LoginSupportView, SupportListView, \
	CreateSupportStartView, CreateSupportFinishView, SupportDetailView, \
	SupportProfileView


urlpatterns = [
	url(r'^$', SupportListView.as_view()),
	url(r'^(?P<id>[0-9]+)/$', SupportDetailView.as_view()),
    url(r'^login/$', LoginSupportView.as_view()),
    url(r'^create-start/$', CreateSupportStartView.as_view()),
    url(r'^create-finish/$', CreateSupportFinishView.as_view())
]