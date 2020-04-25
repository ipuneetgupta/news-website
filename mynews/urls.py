from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^admin/",admin.site.urls),
    url(r"",include('main.urls')),
    url(r"",include('news.urls')),
    url(r"",include('cat.urls')),
    url(r"",include('subcat.urls')),
    url(r"",include('contactform.urls')),
    url(r"",include('trending.urls')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)