from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from django_yaba.blog.models import Story, Links
from django_yaba.blog.feeds import RSSFeed

#info_dict = { 'queryset': Story.objects.all(), 'template_object_name': 'story' }
urlpatterns = patterns('django_yaba.blog.views',
    url(r'^category/(?P<slug>[-\w]+)/$', 'category', name="blog-category"),
    url(r'^$', 'story_list', name="blog-home"),
    url(r'^(?P<slug>[-\w]+)/$', 'story_detail', name="blog-story"),
    url(r'^view/(?P<story_id>[-\w]+)/$', 'story_id', name="blog-id"),
    url(r'^article/(?P<slug>[-\w]+)/$', 'article_detail', name="blog-article"),
    url(r'^search/$', 'search', name="blog-search"),
)

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': {'rss': RSSFeed}}),
    url(r'^links/$', 'links', {'link_dict': {'links': Links}}),
)
