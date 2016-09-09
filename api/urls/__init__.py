from django.conf.urls import url, include

from api.urls import web, mobile


urlpatterns = [
	url(r'^web/', include(web)),
	url(r'^mobile/', include(mobile))

]

