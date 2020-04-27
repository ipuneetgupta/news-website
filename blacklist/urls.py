from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^panel/ip/list/$', views.ip_list, name='ip_list'),
    url(r'^panel/ip/add/$', views.ip_add, name='ip_add'),
    url(r'^panel/ip/del/(?P<pk>\d+)/$', views.ip_del, name='ip_del'),


]  