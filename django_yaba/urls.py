from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.syndication.views import feed
from django_yaba.models import Links
from django_yaba.feeds import RSSFeed

#info_dict = { 'queryset': Story.objects.all(), 'template_object_name': 'story' }
urlpatterns = patterns('django_yaba.views',
    url(r'^category/(?P<slug>[-\w]+)/$', 'category', name="blog-category"),
    url(r'^$', 'story_list', name="blog-home"),
    url(r'^(?P<slug>[-\w]+)/$', 'story_detail', name="blog-story"),
    url(r'^view/(?P<story_id>[-\w]+)/$', 'story_id', name="blog-id"),
    url(r'^article/(?P<slug>[-\w]+)/$', 'article_detail', name="blog-article"),
    url(r'^blog/search/$', 'search', name="blog-search"),
    url(r'^tags/(?P<tag>[-\w]+)/$', 'tag_list', name="blog-tags"),
    url(r'^gallery/list/$', 'gallery_list', name="blog-gallery-list"),
    url(r'^gallery/(?P<slug>[-\w]+)/$', 'gallery', name='blog-gallery'),
    url(r'^gallery/detail/(?P<id>[-\w]+)/$', 'photo_detail', name='photo_detail'),
    url(r'^archives/(?P<date>[-\w]+)/$', 'archives', name='blog-archives'),
    url(r'^status/cache/$', 'cache_view', name='caching'),
)

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': {'rss': RSSFeed}}),
    url(r'^links/$', 'links', {'link_dict': {'links': Links}}),
)

if settings.DJANGO_COMMENTS:
    urlpatterns += patterns('',
        (r'^comments/', include('django.contrib.comments.urls')),
    )
