from django.conf.urls import url

from api.controllers.web.pay import PaysListView, PaysDetailView, \
	PaysHistoryListView


urlpatterns = [
    url(r'^$', PaysListView.as_view()),
    url(r'^(?P<id>[0-9]+)/$', PaysDetailView.as_view()),
    url(r'^history/$', PaysHistoryListView.as_view()),

]