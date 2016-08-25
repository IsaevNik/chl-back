from django.conf.urls import url, include

import support

urlpatterns = [
    url(r'^supports/', include(support))
]