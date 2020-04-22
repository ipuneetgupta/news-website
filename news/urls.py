from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^news/(?P<word>.*)/$', views.news_detail, name='news_detail'),
    url(r'^panel/news/list/$', views.news_list, name='news_list'),
]