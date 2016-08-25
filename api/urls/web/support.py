from django.conf.urls import url


from api.controllers.support import AuthSupportView, SupportListView, \
	CreateSupportStartView, CreateSupportFinishView

urlpatterns = [
	url(r'^$', SupportListView.as_view()),
    url(r'^auth/$', AuthSupportView.as_view()),
    url(r'^create-start/$', CreateSupportStartView.as_view()),
    url(r'^create-finish/$', CreateSupportFinishView.as_view())
]