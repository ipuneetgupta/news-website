from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^newsletter/add/$', views.news_letter, name='news_letter'),
    url(r'^panel/newsletter/emails/$', views.news_letter_email, name='news_letter_email'),
    url(r'^panel/newsletter/phones/$', views.news_letter_phone, name='news_letter_phone'),
    url(r'^panel/newsletter/del/(?P<pk>\d+)/(?P<num>\d+)/$', views.news_letter_del, name='news_letter_del'),



]