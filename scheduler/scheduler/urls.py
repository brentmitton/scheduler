from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^course/', include('courses.urls')),
    url(r'^$', 'courses.views.index', name='index'),
)
