from django.conf.urls import url , include
from . import views

urlpatterns = [
       url(r'^panel/category/list/$', views.cat_list, name='cat_list'),
       url(r'^panel/category/add/$', views.cat_add, name='cat_add'),
       url(r'^export/cat/csv/$', views.export_cat_csv, name='export_cat_csv'),
       url(r'^import/cat/csv/$', views.import_cat_csv, name='import_cat_csv'),
       url(r'^panel/category/del/(?P<pk>\d+)/$', views.cat_del, name='cat_del'),

]