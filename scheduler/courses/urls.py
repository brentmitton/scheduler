from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('courses.views',
        url(r'^scrape/(?P<semester>\d+)/$', 'scrape', name='scrape'),
        url(r'^(?P<semester>\d+)/(?P<dept>\d+)', 'dept_sem_list', name='dept_sem_list'),
        url(r'^(?P<semester>\d+)/', 'semester_list', name='semester_list'),
        url(r'^dept/(?P<dept>\d+)', 'dept_list', name='dept_list'),
        url('/$', 'semester_list'),
        )
