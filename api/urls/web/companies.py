from django.conf.urls import url


from api.controllers.web.company import RegCompanyStartView, CompanyStatisticView, \
	CompanyDetailView

urlpatterns = [
	url(r'^$', CompanyStatisticView.as_view()),
	url(r'^(?P<id>[0-9]+)/$', CompanyDetailView.as_view()),
    url(r'^registration-start/$', RegCompanyStartView.as_view())
]