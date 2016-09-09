from django.conf.urls import url, include

import agent


urlpatterns = [
    url(r'^agent/', include(agent)),

]