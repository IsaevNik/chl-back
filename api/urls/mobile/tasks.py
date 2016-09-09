from django.conf.urls import url


from api.controllers.task_address import WithoutAddressTaskView, WithAddressTaskView


urlpatterns = [
	url(r'^without-address/$', WithoutAddressTaskView.as_view()),
	url(r'^with-address/$', WithAddressTaskView.as_view()),
]