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
    url(r'^get_items_by_category/(?P<category>\w+)$','cbayweb.views.get_items_by_category', name='get_items_by_category'),
    url(r'^searchItem$','cbayweb.views.searchItem', name='searchItem'),
    url(r'^editProfile$','cbayweb.views.editProfile', name='editProfile'),
    url(r'^id_picture/(?P<id>\d+)$', 'cbayweb.views.id_picture', name='id_picture'),
    url(r'^addComment$', 'cbayweb.views.addComment', name='addComment'),
    url(r'^confirmDelivery$', 'cbayweb.views.confirmDelivery', name = 'confirmDelivery'),
    url(r'^sendMessage$', 'cbayweb.views.sendMessage', name = 'sendMessage'),
    url(r'^viewMessage$', 'cbayweb.views.viewMessage', name='viewMessage'),
    url(r'^addToShoppingCart$','cbayweb.views.addToShoppingCart', name='addToShoppingCart'),
    url(r'^viewShoppingCart$','cbayweb.views.viewShoppingCart', name='viewShoppingCart'),
    url(r'^deleteOrder$','cbayweb.views.deleteOrder', name='deleteOrder'),
    url(r'^checkOutShoppingCart$','cbayweb.views.checkOutShoppingCart', name='checkOutShoppingCart'),
    url(r'^viewProfile/(?P<user_id>\d+)$', 'cbayweb.views.viewProfile', name='viewProfile'),
    url(r'^messagePicture/(?P<message_id>\d+)$', 'cbayweb.views.messagePicture', name='messagePicture'),
    url(r'^followUser$', 'cbayweb.views.addToFollowing', name='addToFollowing'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'cbayweb.views.confirmRegistration', name='confirm'),
    url(r'^accounts/password_change/$', 
        'django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/accounts/password_change/done/'}, 
        name="password_change"), 
    (r'^accounts/password_change/done/$', 
        'django.contrib.auth.views.password_change_done'),

    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),
    (r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/password_reset/complete/'}, name="password_reset_confirm"),
    (r'^accounts/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete'),
)