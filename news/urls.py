from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^news/(?P<word>.*)/$',views.news_detail,name='news_detail'),
]