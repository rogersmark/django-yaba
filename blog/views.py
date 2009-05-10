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
    link_list = Links.objects.all()
    return render_to_response("blog/story_list.html", {'posts':posts, 'link_list': link_list})

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
    return render_to_response("blog/story_list.html", {'posts': posts, 'link_list': link_list, 'articles': articles})

def story_detail(request, slug):
    posts = get_object_or_404(Story, slug=slug)
    link_list = Links.objects.all()
    articles = Article.objects.all()
    return render_to_response("blog/story_detail.html", {'posts': posts, 'link_list': link_list, 'articles': articles})

def article_detail(request, slug):
    posts = get_object_or_404(Article, slug=slug)
    link_list = Links.objects.all()
    articles = Article.objects.all()
    return render_to_response("blog/story_detail.html", {'posts': posts, 'link_list': link_list, 'articles': articles})

def links(request):
    """ Display Links """
    link_list = Lists.objects.all()
    return render_to_response("blog/story_list.html", {'links': links})

