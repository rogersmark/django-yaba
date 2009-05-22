import feedparser
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django_yaba.blog.models import *

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

def category(request, slug):
    """Given a category slug, display all items in a category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Paginator(Story.objects.filter(category=category), 10)
    page = int(request.GET.get('page', '1'))
    heading = "Category: %s" % category.label
    link_list = Links.objects.all()
    articles = Article.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    return render_to_response("blog/story_list.html", {'posts':posts, 'link_list': link_list, 'articles': articles, 'commit': commit, 'sitename': sitename})

def search(request):
    if 'q' in request.GET:
        term = request.GET['q']
        posts = Story.objects.filter(Q(title__contains=term))
        heading = "Search results"

    return render_to_response("blog/story_list.html", {'posts': posts})

def story_list(request):
    paginator = Paginator(Story.objects.all().order_by('-created'), 5)
    page = int(request.GET.get('page', '1'))
    posts = paginator.page(page)
    link_list = Links.objects.all()
    articles = Article.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts': posts, 'sitename': sitename})

def story_detail(request, slug):
    posts = get_object_or_404(Story, slug=slug)
    link_list = Links.objects.all()
    articles = Article.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_detail.html", {'posts': posts, 'link_list': link_list, 'articles': articles, 'commit': commit, 'sitename': sitename, 'ROOT_URL': ROOT_URL})

def article_detail(request, slug):
    posts = get_object_or_404(Article, slug=slug)
    link_list = Links.objects.all()
    articles = Article.objects.all()
    commit = parse_github()
    sitename = settings.BLOG_NAME
    ROOT_URL = settings.ROOT_BLOG_URL
    return render_to_response("blog/story_detail.html", {'posts': posts, 'link_list': link_list, 'articles': articles, 'commit': commit, 'sitename': sitename, 'ROOT_URL': ROOT_URL})

def links(request):
    """ Display Links """
    link_list = Lists.objects.all()
    return render_to_response("blog/story_list.html", {'links': links})

