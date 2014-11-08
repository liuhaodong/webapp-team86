from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^homepage$','cbayweb.views.homepage',name='homepage'),
    url(r'^viewItem$','cbayweb.views.viewItem',name='viewItem'),
)
