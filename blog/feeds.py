from django.contrib.syndication.feeds import Feed
from newblog.blog.models import Story

class RSSFeed(Feed):
    title = "..::newblog studios::.."
    description = "Recent Posts"
#    link = "http://www.newblog.com/"
#    item_link = link

    def items(self):
        return Story.objects.all().order_by('-created')[:10]

