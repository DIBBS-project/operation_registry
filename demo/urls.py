from django.conf.urls import url, include
from demo import views


urlpatterns = [
    url(r'^processdef_form/',  views.create_processdef, name='processdef_form'),
    url(r'^processdefs/',  views.processdefs, name='processdefs'),
]
