from django.conf.urls import patterns, url
from .views import Home, NewList, GetLists, AddToList, RemoveFromList

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^lists/new/$', NewList.as_view(), name='list_new'),
    url(r'^lists/getall/$', GetLists.as_view(), name='list_getall'),
    url(r'^lists/add/$', AddToList.as_view(), name='list_add'),
    url(r'^lists/remove/$', RemoveFromList.as_view(), name='list_remove'),
)
