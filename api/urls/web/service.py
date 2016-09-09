from django.conf.urls import url, include

from api.controllers.service import uploadImg

urlpatterns = [
    url(r'^upload-img/$', uploadImg),
]