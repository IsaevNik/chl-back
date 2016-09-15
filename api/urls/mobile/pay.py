from django.conf.urls import url


from api.controllers.mobile.pay import PayListView, PayDetailView


urlpatterns = [
	url(r'^$', PayListView.as_view()),
	url(r'^(?P<id>[0-9]+)/$', PayDetailView.as_view())
]