from django.conf.urls import url, include
from demo import views


urlpatterns = [
    url(r'^processdef_form/',  views.create_processdef),
    url(r'^processdefs/',  views.processdefs),
    url(r'^processimpl_form/',  views.create_processimpl),
    url(r'^processimpls/',  views.processimpls),
]
