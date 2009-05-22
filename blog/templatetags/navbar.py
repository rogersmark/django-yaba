from django_yaba.blog.models import *
from django.conf import settings
from django import template

register = template.Library

def parse_github():
    """ Grab latest commits from GitHub """
    d = feedparser.parse("http://github.com/%s.atom" % settings.GITHUB_USERNAME)
    e = d.entries[:5]
    commit = "<ul>"
    for x in e:
        commit += "<p><li>"
        commit += '<a href="%s">' % x['link']
        commit += x['title_detail']['value']
        commit += "</a>\n@ %s" % x['updated']
        commit += "</li></p>"
    commit += "</ul>"
    return commit

@register.simple_tag
def menu_system(format_string):
    link_list = Links.objects.all()
    articles = Article.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    ROOT_URL = settings.ROOT_BLOG_URL
    return {'link_list': link_list, 'articles': articles, 'commit': commit, 'sitename': sitename, 'ROOT_URL': ROOT_URL}
