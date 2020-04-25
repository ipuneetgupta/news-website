from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^panel/setting/$', views.site_setting, name='site_setting'),
    url(r'^panel/about/setting/$', views.about_setting, name='about_setting'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^panel/change/pass/$', views.change_pass, name='change_pass'),
    url(r'^register/$', views.myregister, name='myregister'),

]