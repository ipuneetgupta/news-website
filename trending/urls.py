from django.conf.urls import url , include
from . import views

urlpatterns = [
  
url(r'^panel/trending/add/$', views.trending_add, name='trending_add'),
url(r'^panel/trending/edit/(?P<pk>\d+)/$', views.trending_edit, name='trending_edit'),
url(r'^panel/trending/del/(?P<pk>\d+)/$', views.trending_del, name='trending_del'),


]