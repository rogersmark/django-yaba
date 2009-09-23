from django.template import Library, Node, TemplateSyntaxError
from django.core.cache import cache
from django.conf import settings
from datetime import datetime
from time import mktime, strptime
import urllib
import simplejson

register = Library()

class CachedNode(Node):
    """
    Cached template node.

    Subclasses should define the methods ``get_cache_key()`` and
    ``get_content()`` instead of the standard render() method. Subclasses may
    also define the class attribute ``cache_timeout`` to override the default
    cache timeout of ten minutes.
    """

    cache_timeout = 600

    def render(self, context):
        if settings.DEBUG:
            return self.get_content(context)
        key = self.get_cache_key(context)
        content = cache.get(key)
        if not content:
            content = self.get_content(context)
            cache.set(key, content, self.cache_timeout)
        return content

    def get_cache_key(self, context):
        raise NotImplementedError()

    def get_content(self, context):
        raise NotImplementedError()

class ContextUpdatingNode(Node):
    """
    Node that updates the context with certain values.

    Subclasses should define ``get_content()``, which should return a dictionary
    to be added to the context.
    """

    def render(self, context):
        context.update(self.get_content(context))
        return ''

class CachedContextUpdatingNode(CachedNode, ContextUpdatingNode):
    """
    Node that updates the context, and is cached. Subclasses need to define
    ``get_cache_key()`` and ``get_content()``.
    """

    def render(self, context):
        context.update(CachedNode.render(self, context))
        return ''

class TwitterNode(CachedContextUpdatingNode):
    """
    Node that gets the twitter public user timeline
    """

    cache_timeout = 1800 # 30 Minutes, maybe you want to change this

    def __init__(self, username, varname):
        self.username = settings.TWITTER_USERNAME
        self.varname = varname

    def make_datetime(self, created_at):
        return datetime.fromtimestamp(mktime(strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')))

    def get_cache_key(self, context):
        return 'twitter_user_timeline_cache'

    def get_content(self, context):
        try:
            response = urllib.urlopen('http://twitter.com/statuses/user_timeline/%s.json' % self.username).read()
            json = simplejson.loads(response)[:5]
        except:
            return {self.varname : None}
        for i in range(len(json)):
            json[i]['created_at'] = self.make_datetime(json[i]['created_at'])
        return {self.varname : json}

@register.tag
def twitter_user_timeline(parser, token):
    """
    Usage:
    {% twitter_user_timeline username as twitter_entries %}
    {% if twitter_entries %}{% for entry in twitter_entries %}
    <p>{{ entry.created_at|date:"d M Y H:i" }} - {{ entry.text }}</p>
    {% endfor %}{% endif %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "twitter_user_timeline tag takes exactly three arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to twitter_user_timeline tag must be 'as'"
    return TwitterNode(bits[1], bits[3])

