from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
   url(r'^(?P<pk>\d+)/$', views.entry_detail, name="entry_detail"),
)
