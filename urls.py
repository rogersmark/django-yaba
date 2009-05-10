from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^', include('django_yaba.blog.urls')),
    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/home/f4nt/git-repos/personal/django_yaba/media/'}),
)
