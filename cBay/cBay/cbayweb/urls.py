from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$','cbayweb.views.homepage',name='homepage'),
    url(r'^revieworder$','cbayweb.views.reviewOrder',name='reviewOrder'),
)
