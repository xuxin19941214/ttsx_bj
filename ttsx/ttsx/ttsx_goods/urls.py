
#coding=utf-8
from django.conf.urls import url

import views
from search_view import MySearchView
urlpatterns = [
    url('^$', views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.goods_list),#下划线防止贪婪
    url(r'^(\d+)/$', views.detail),
    url(r'^index/$', views.index),
    url(r'^search/$',MySearchView.as_view())
]
