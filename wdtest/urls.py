from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('', include('imglist.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
