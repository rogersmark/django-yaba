from django.contrib.syndication.feeds import Feed
from django_yaba.blog.models import Story

class RSSFeed(Feed):
    title = "..::f4ntasmic studios::.."
    description = "Recent Posts"
    link = "http://www.django_yaba.com/"
    item_link = link

    def items(self):
        return Story.objects.all().order_by('-created')[:10]

