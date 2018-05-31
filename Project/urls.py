from django.conf.urls import include, url
from Project import views
from django.views.static import serve
from django.conf import settings

from django.contrib import admin

urlpatterns =[
    url(r'^$',views.home , name='home'),
    url(r'^([0-9]+)/$',views.details , name='details'),
    url(r'^delete/([0-9]+)/$',views.delete, name='delete'),
    url(r'^search/$', views.book_search, name='book_search'),
    url(r'^borrow/([0-9]+)/$', views.book_borrow, name='book_borrow'),
    url(r'^return/([0-9]+)/$', views.book_return, name='book_return'),
    url(r'^comment/([0-9]+)/$', views.book_comment, name='book_comment'),
    url(r'^add_book/$', views.book_add, name='book_add'),
    url(r'^update/([0-9]+)/$',views.book_update, name='book_update'),
    url(r'^check/$', views.check, name='check'),
    ]
if settings.DEBUG:
    urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve,
    {'document_root': settings.MEDIA_ROOT,}),
]