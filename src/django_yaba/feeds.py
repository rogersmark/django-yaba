from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django_yaba.models import Story

class RSSFeed(Feed):
    title = settings.BLOG_NAME
    description = "Recent Posts"
    link = settings.ROOT_BLOG_URL

    def items(self):
        return Story.objects.all().order_by('-created')[:10]
    
