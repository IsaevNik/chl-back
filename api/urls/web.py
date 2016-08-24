from django.conf.urls import url

from api.controllers.auth import AuthView, SupportView, CreateSupportStartView

urlpatterns = [
    url(r'^login/$', AuthView.as_view()),
    url(r'^support/$', SupportView.as_view()),
    url(r'^create/$', CreateSupportStartView.as_view())
]