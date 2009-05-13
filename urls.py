from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^', include('django_yaba.blog.urls')),
)
