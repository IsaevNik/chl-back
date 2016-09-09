from django.conf.urls import url, include

import agent
import tasks
import task

urlpatterns = [
    url(r'^agent/', include(agent)),
    url(r'^tasks/', include(tasks)),
    url(r'^task/', include(task))

]