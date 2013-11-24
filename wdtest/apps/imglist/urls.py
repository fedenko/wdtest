from django.conf.urls import patterns, url
from .views import Home, AddList

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^lists/add/$', AddList.as_view(), name='list_add'),
)
