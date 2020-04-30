from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    url(r"^admin/",admin.site.urls),

    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),


    url(r"",include('main.urls')),
    url(r"",include('news.urls')),
    url(r"",include('cat.urls')),
    url(r"",include('subcat.urls')),
    url(r"",include('contactform.urls')),
    url(r"",include('trending.urls')),
    url(r"",include('manager.urls')),
    url(r"",include('newsletter.urls')),
    url(r"",include('comment.urls')),
    url(r"",include('blacklist.urls')),

]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)