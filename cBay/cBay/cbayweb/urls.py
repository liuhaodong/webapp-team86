from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^homepage$','cbayweb.views.homepage',name='homepage'),
    url(r'^viewSale/(?P<sale_id>\d+)$','cbayweb.views.viewSale',name='viewSale'),
    url(r'^viewAuction/(?P<auction_id>\d+)$','cbayweb.views.viewAuction',name='viewAuction'),
    url(r'^register$','cbayweb.views.register',name='register'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'cbayweb/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^reviewOrder$','cbayweb.views.reviewOrder',name='reviewOrder'),
    url(r'^postSale$','cbayweb.views.postSale',name='postSale'),
    url(r'^postAuction$','cbayweb.views.postAuction',name='postAuction'),
    url(r'^accountManage$','cbayweb.views.accountManage',name='accountManage'),
    url(r'^placeOrder$','cbayweb.views.placeOrder',name='placeOrder'),
    url(r'^placeBid$','cbayweb.views.placeBid',name='placeBid'),
    url(r'^payOrder$','cbayweb.views.payOrder',name='payOrder'),
    url(r'^item_picture/(?P<sale_id>\d+)$', 'cbayweb.views.get_item_picture', name='item_picture'),
    url(r'^auction_picture/(?P<auction_id>\d+)$', 'cbayweb.views.get_auction_picture', name='auction_picture'),
    url(r'^check_auction/(?P<auction_id>\d+)$', 'cbayweb.views.check_auction', name='check_auction'),
    url(r'^buyAuction', 'cbayweb.views.buy_auction', name='buyAuction'),
)