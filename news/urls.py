from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^news/(?P<word>.*)/$', views.news_detail, name='news_detail'),
    url(r'^panel/news/list/$', views.news_list, name='news_list'),
    url(r'^panel/news/add/$', views.add_news, name='add_news'),
    url(r'^panel/news/del/(?P<pk>\d+)/$', views.news_delete, name='news_delete'),
    url(r'^panel/news/edit/(?P<pk>\d+)/$', views.news_edit, name='news_edit'),
    url(r'^panel/news/publish/(?P<pk>\d+)/$', views.news_publish, name='news_publish'),
    url(r'^url/?short=/(?P<randNum>\d+)/$', views.news_detail_shorturl, name='news_detail_shorturl'),
    url(r'^all/news/(?P<word>.*)/$', views.news_all_show, name='news_all_show'),
    url(r'^all/news/$', views.all_news, name='all_news'),
    url(r'^search/$', views.all_news_search, name='all_news_search'),
    url(r'^update/news/list/$', views.update_list, name='update_list'),

]