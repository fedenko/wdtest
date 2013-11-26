from django.conf.urls import patterns, url
from .views import Home, AddList, GetLists, RemoveFromList

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^lists/add/$', AddList.as_view(), name='list_add'),
    url(r'^lists/get/$', GetLists.as_view(), name='list_getall'),
    url(r'^lists/remove/$', RemoveFromList.as_view(), name='list_rmfrom'),
)
