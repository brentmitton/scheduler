from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('courses.views',
        url(r'^scrape/(?P<semester>\d+)/$', 'scrape', name='scrape'),
        )
