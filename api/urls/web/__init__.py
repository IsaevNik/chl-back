from django.conf.urls import url, include

import support

urlpatterns = [
    url(r'^support/', include(support))
]