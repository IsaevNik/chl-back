from django.conf.urls import url, include

import supports
import company
from api.controllers.support import SupportProfileView


urlpatterns = [
    url(r'^supports/', include(supports)),
    url(r'^support/$', SupportProfileView.as_view()),
    url(r'^company/', include(company))
]