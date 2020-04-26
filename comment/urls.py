from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^comment/add/news/(?P<pk>\d+)/$', views.cm_add_news, name='cm_add_news'),
    url(r'^panel/comments/list/$', views.comments_list, name='comments_list'),
    url(r'^panel/comment/del/(?P<pk>\d+)/$', views.comment_del, name='comment_del'),
    url(r'^panel/comment/confirme/(?P<pk>\d+)/$', views.comment_status, name='comment_status'),

]  