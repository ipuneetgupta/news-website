from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^panel/manager/list/$', views.manager_list, name='manager_list'),
    url(r'^panel/manager/del/(?P<pk>\d+)/$', views.manager_del, name='manager_del'),
    url(r'^panel/manager/group/$', views.manager_group, name='manager_group'),
    url(r'^panel/manager/perms/$', views.manager_perms, name='manager_perms'),
    url(r'^panel/manager/perms/del/(?P<name>.*)/$', views.manager_perms_del, name='manager_perms_del'),
    url(r'^panel/manager/group/add/$', views.manager_group_add, name='manager_group_add'),
    url(r'^panel/manager/group/del/(?P<name>.*)/$', views.manager_group_del, name='manager_group_del'),
    url(r'^panel/manager/show/(?P<pk>\d+)/$', views.users_groups, name='users_groups'),
    url(r'^panel/manager/addtogroup/(?P<pk>\d+)/$', views.add_users_to_groups, name='add_users_to_groups'),
    url(r'^panel/manager/delgroup/(?P<pk>\d+)/(?P<name>.*)/$', views.del_users_to_groups, name='del_users_to_groups'),
    url(r'^panel/manager/perms/(?P<pk>\d+)/$', views.users_perms, name='users_perms'),
    url(r'^panel/manager/perms/add/$', views.manager_perms_add, name='manager_perms_add'),
    url(r'^panel/manager/delperms/(?P<pk>\d+)/(?P<name>.*)/$', views.users_perms_del, name='users_perms_del'),
    url(r'^panel/manager/addtoperms/(?P<pk>\d+)/$', views.users_perms_add, name='users_perms_add'),
    url(r'^panel/manager/addpermstogroup/(?P<name>.*)/$', views.groups_perms, name='groups_perms'),
    url(r'^panel/manager/delpermsfromgroup/(?P<gname>.*)/(?P<pname>.*)/$', views.groups_perms_del, name='groups_perms_del'),
    url(r'^panel/manager/grouppermsadd/(?P<gname>.*)/$', views.groups_perms_add, name='groups_perms_add'),



]