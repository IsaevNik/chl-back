from django.conf.urls import url, include

from api.urls import web

urlpatterns = [
	url(r'^web/', include(web))
]