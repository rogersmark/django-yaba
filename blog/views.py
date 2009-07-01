import logging
from django_yaba.blog.multiquery import MultiQuerySet
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django_yaba.blog.models import Story, Article, Category, Links, Photo, Gallery

LOG_FILENAME = '/tmp/yaba.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

def sort_by_date(x):
    return x.created

def category(request, slug):
    """Given a category slug, display all items in a category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Paginator(Story.objects.filter(category=category), 10)
    page = int(request.GET.get('page', '1'))
    heading = "Category: %s" % category.label
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts':posts, 'ROOT_URL': ROOT_URL})

def story_list(request):
    """ Lists all stories and galleries starting with the most recent. Currently through them into a MultiQuerySet and then we sort them """
    stories = Story.objects.all().order_by('-created')
    galleries = Gallery.objects.all().order_by('-created')
    temp = MultiQuerySet(stories, galleries)
    front_page = []
    for x in temp:
        front_page.append(x)
    
    front_page.sort(key=sort_by_date, reverse=1)
    paginator = Paginator(front_page, 5)
    page = int(request.GET.get('page', '1'))
    posts = paginator.page(page)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def story_detail(request, slug):
    """ Takes the slug of a story, and displays that story """
    posts = get_object_or_404(Story, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def article_detail(request, slug):
    """ Takes the slug of an article and displays that article """
    posts = get_object_or_404(Article, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/article_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def links(request):
    """ Display Links - Deprecated"""
    link_list = Links.objects.all()
    return render_to_response("blog/story_list.html", {'links': links})

def story_id(request, story_id):
    """ Bit of a cheap hack. Currently used to get people back to the story they commented on. Translates an ID to a slug """
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

def search(request):
    """ searches across galleries, articles, and blog posts 
         TODO: Add Galleries to this
    """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    if 'q' in request.GET:
        term = request.GET['q']
        post_list = Story.objects.filter(Q(title__icontains=term) | Q(body__icontains=term))
        articles = Article.objects.filter(Q(title__icontains=term) | Q(body__icontains=term))
        galleries = Gallery.objects.filter(Q(title__icontains=term) | Q(body__icontains=term))
        temp = MultiQuerySet(post_list, articles, galleries)
        front_page = []
        for x in temp:
            front_page.append(x)
    
        front_page.sort(key=sort_by_date, reverse=1)
        paginator = Paginator(front_page, 5)
        page = int(request.GET.get('page', '1'))
        posts = paginator.page(page)
        return render_to_response("blog/story_search.html", {'posts': posts, "articles": articles, 'galleries': galleries, 'ROOT_URL': ROOT_URL})

    else:
       return HttpResponseRedirect('/')

def tag_list(request, tag):
    """ Accepts a tag, and finds all stories that match it. 
         TODO: Add galleries and articles to this 
    """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    post_list = Paginator(Story.objects.filter(tags__icontains=tag), 5)
    page = int(request.GET.get('page', '1'))
    posts = post_list.page(page)
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL})

def gallery(request, slug):
    """ Accepts a slug, and grabs the article that matches that """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    gallery = get_object_or_404(Gallery, slug=slug)
    return render_to_response("blog/gallery.html", {'gallery': gallery, 'ROOT_URL': ROOT_URL})

def photo_detail(request, id):
    """ Deprecated """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    photo = get_object_or_404(Photo, id=id)
    return render_to_response("blog/photo.html", {'photo': photo, 'ROOT_URL': ROOT_URL})

def gallery_list(request):
    """ Paginates all galleries """
    paginator = Paginator(Gallery.objects.all().order_by('-created'), 5)
    page = int(request.GET.get('page', '1'))
    gallery = paginator.page(page)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/gallery_list.html", {'gallery': gallery, 'ROOT_URL': ROOT_URL})

def archives(request, date):
    """ Accepts a date in YYYY-MM format, and returns all stories matching that.  
          TODO: Add galleries and articles to this
    """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    post_list = Paginator(Story.objects.filter(created__icontains=str(date)), 5)
    page = int(request.GET.get('page', '1'))
    posts = post_list.page(page)
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL})
