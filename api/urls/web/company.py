from django.conf.urls import url


from api.controllers.company import CompanyView, RegCompanyStartView, \
    RegCompanyFinishView, CompanyStatisticView

urlpatterns = [
	url(r'^$',CompanyView.as_view()),
    url(r'^registration-start/$', RegCompanyStartView.as_view()),
    url(r'^registration-finish/$', RegCompanyFinishView.as_view())
]