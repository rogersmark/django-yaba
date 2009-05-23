import feedparser
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django_yaba.blog.models import *

def category(request, slug):
    """Given a category slug, display all items in a category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Paginator(Story.objects.filter(category=category), 10)
    page = int(request.GET.get('page', '1'))
    heading = "Category: %s" % category.label
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts':posts, 'ROOT_URL': ROOT_URL})

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
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def story_detail(request, slug):
    posts = get_object_or_404(Story, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def article_detail(request, slug):
    posts = get_object_or_404(Article, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/article_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def links(request):
    """ Display Links """
    link_list = Lists.objects.all()
    return render_to_response("blog/story_list.html", {'links': links})

def story_id(request, story_id):
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    try:
        posts = get_object_or_404(Story, pk=story_id)
        title = posts.slug
        return HttpResponseRedirect("/%s/" % title)
    except ObjectDoesNotExist:
        pass

    try:
        posts = get_object_or_404(Article, pk=story_id)
        title = posts.slug
        return HttpResponseRedirect("/%s/" % title)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/")
