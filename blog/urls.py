from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from newblog.blog.models import Story, Links
from newblog.blog.feeds import RSSFeed

#info_dict = { 'queryset': Story.objects.all(), 'template_object_name': 'story' }
urlpatterns = patterns('newblog.blog.views',
    url(r'^category/(?P<slug>[-\w]+)/$', 'category', name="blog-category"),
    url(r'^$', 'story_list', name="blog-home"),
    url(r'^(?P<slug>[-\w]+)/$', 'story_detail', name="blog-story"),
    url(r'^search/$', 'search', name="blog-search"),
)

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': {'rss': RSSFeed}}),
    url(r'^links/$', 'links', {'link_dict': {'links': Links}}),
)
