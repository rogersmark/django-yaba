import feedparser
import datetime
from django_yaba.models import *
from django.conf import settings
from django import template

register = template.Library()

def parse_github():
    if settings.GITHUB_USERNAME:
        """ Grab latest commits from GitHub """
        d = feedparser.parse("http://github.com/%s.atom" % settings.GITHUB_USERNAME)
        e = d.entries[:5]
        commit = "<ul>"
        for x in e:
            link = x['link']
            link = link.lstrip("http://github.com/")
            link = "http://github.com/%s" % link
            commit += "<p><li>"
            commit += '<a href="%s">' % link
            commit += x['title_detail']['value']
            commit += "</a>\n@ %s" % x['updated']
            commit += "</li></p>"
        commit += "</ul>"
        return commit
    else:
        commit = False
        return commit

def theme():
    theme = Configuration.objects.all()[0].theme.slug
    theme = theme.rstrip()
    return {'theme': theme}

def sitename():
    sitename = settings.BLOG_NAME
    return {'sitename': sitename}

def archives():
    """ Creating Archives navigation for the side bar. We start by grabbing all the content, which needs to be made more effecient. 
    Then we parse out the year date times, then the month date times. """ 
    stories = Story.objects.all()
    galleries = Gallery.objects.all()
    articles = Article.objects.all()
    created = datetime.datetime(2000, 1, 1)
    
    year_range = []
    for x in stories.dates('created', 'year'):
        if x not in year_range:
            year_range.append(x)
    for x in galleries.dates('created', 'year'):
        if x not in year_range:
            year_range.append(x)
    for x in articles.dates('created', 'year'):
        if x not in year_range:
            year_range.append(x)
        
    year_range.sort()
    
    month_range = []
    for x in stories.dates('created', 'month'):
        if x not in month_range:
            month_range.append(x)
    for x in galleries.dates('created', 'month'):
        if x not in month_range:
            month_range.append(x)
    for x in articles.dates('created', 'month'):
        if x not in month_range:
            month_range.append(x)
    
    month_range.sort()
    
    return year_range, month_range

def sidebar():
    categories = Category.objects.all()
    link_list = Links.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    year_range, month_range = archives()
    if settings.TWITTER_USERNAME or settings.TWITTER_PASSWORD:
        tweet = True
    else:
        tweet = False

    return {'link_list': link_list, 'commit': commit, 'sitename': sitename, 'categories': categories, 'tweet_it': tweet, 'tweet_user': settings.TWITTER_USERNAME, 'year_range': year_range, 'month_range': month_range}

def main_nav():
    articles = Article.objects.all()
    return {'articles': articles}

register.inclusion_tag('sidebar.html')(sidebar)
register.inclusion_tag('main_nav.html')(main_nav)
register.inclusion_tag('sitename.html')(sitename)
register.inclusion_tag('theme.html')(theme)
