from django.conf.urls import url, include

from api.controllers.web.subscription import SubscriptionListView, SubscriptionDetailView, \
	put_order_id

urlpatterns = [
    url(r'^$', SubscriptionListView.as_view()),
    url(r'^(?P<id>[0-9]+)/$', SubscriptionDetailView.as_view()),
    url(r'^put_order_id/$', put_order_id)
]