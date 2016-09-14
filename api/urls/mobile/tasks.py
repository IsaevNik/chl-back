from django.conf.urls import url


from api.controllers.mobile.task import WithoutAddressTaskView, WithAddressTaskView


urlpatterns = [
	url(r'^without-address/$', WithoutAddressTaskView.as_view()),
	url(r'^with-address/$', WithAddressTaskView.as_view()),
]