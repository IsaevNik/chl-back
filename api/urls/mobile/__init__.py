from django.conf.urls import url, include

import agent
import tasks
import task
import inwork
import pay

urlpatterns = [
    url(r'^agent/', include(agent)),
    url(r'^tasks/', include(tasks)),
    url(r'^task/', include(task)),
    url(r'^inwork/', include(inwork)),
    url(r'^pays/', include(pay))

]