import logging
import datetime, re
from django import http
from django.views.decorators.cache import cache_page
from django_yaba.multiquery import MultiQuerySet
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django_yaba.models import Story, Article, Category, Links, Photo, Gallery
from django.template import RequestContext 

LOG_FILENAME = '/tmp/yaba.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

def sort_by_date(x):
    return x.created

@cache_page(15 * 10)
def category(request, slug):
    """Given a category slug, display all items in a category"""
    category = get_object_or_404(Category, slug=slug)
    galleries = Gallery.objects.filter(category=category)
    articles = Article.objects.filter(category=category)
    stories = Story.objects.filter(category=category)
    temp = MultiQuerySet(stories, galleries, articles)
    front_page = []
    for x in temp:
        front_page.append(x)
        
    front_page.sort(key=sort_by_date, reverse=1)
    paginator = Paginator(front_page, 10)
    page = int(request.GET.get('page', '1'))
    posts = paginator.page(page)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_list.html", {'posts':posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

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
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def story_detail(request, slug):
    """ Takes the slug of a story, and displays that story """
    posts = get_object_or_404(Story, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/story_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def article_detail(request, slug):
    """ Takes the slug of an article and displays that article """
    posts = get_object_or_404(Article, slug=slug)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/article_detail.html", {'posts': posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def links(request):
    """ Display Links - Deprecated"""
    link_list = Links.objects.all()
    return render_to_response("blog/story_list.html", {'links': links}, context_instance=RequestContext(request))

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
    """ searches across galleries, articles, and blog posts  """
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
        return render_to_response("blog/story_search.html", {'posts': posts, "articles": articles, 'galleries': galleries, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

    else:
       return HttpResponseRedirect('/')

def tag_list(request, tag):
    """ Accepts a tag, and finds all stories that match it.  """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    stories = Story.objects.filter(tags__icontains=tag)
    galleries = Gallery.objects.filter(tags__icontains=tag)
    articles = Article.objects.filter(tags__icontains=tag)
    temp = MultiQuerySet(stories, galleries, articles)
    front_page = []
    for x in temp:
        front_page.append(x)
    
    front_page.sort(key=sort_by_date, reverse=1)
    paginator = Paginator(front_page, 5)
    page = int(request.GET.get('page', '1'))
    posts = paginator.page(page)
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

@cache_page(15 * 60)
def gallery(request, slug):
    """ Accepts a slug, and grabs the article that matches that """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    gallery = get_object_or_404(Gallery, slug=slug)
    return render_to_response("blog/gallery.html", {'gallery': gallery, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def photo_detail(request, id):
    """ Deprecated """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    photo = get_object_or_404(Photo, id=id)
    return render_to_response("blog/photo.html", {'photo': photo, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

@cache_page(15 * 30)
def gallery_list(request):
    """ Paginates all galleries """
    paginator = Paginator(Gallery.objects.all().order_by('-created'), 5)
    page = int(request.GET.get('page', '1'))
    gallery = paginator.page(page)
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    return render_to_response("blog/gallery_list.html", {'gallery': gallery, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def archives(request, date):
    """ Accepts a date in YYYY-MM format, and returns all stories matching that.  """
    ROOT_URL = settings.ROOT_BLOG_URL
    ROOT_URL = ROOT_URL.rstrip("/")
    stories = Story.objects.filter(created__icontains=str(date))
    galleries = Gallery.objects.filter(created__icontains=str(date))
    articles = Article.objects.filter(created__icontains=str(date))
    temp = MultiQuerySet(stories, galleries, articles)
    front_page = []
    for x in temp:
        front_page.append(x)
    
    front_page.sort(key=sort_by_date, reverse=1)
    paginator = Paginator(front_page, 5)
    page = int(request.GET.get('page', '1'))
    posts = paginator.page(page)
    return render_to_response("blog/story_list.html", {'posts': posts, 'ROOT_URL': ROOT_URL}, context_instance=RequestContext(request))

def cache_view(request):
    """
    Tries to import memcache, fails out if it can't and raises a 404. Also
    raises a 404 in the case of unauthenticated users, or memcache not
    being used. Graciously borrowed from:
    http://effbot.org/zone/django-memcached-view.htm
    """
    try:
        import memcache
    except ImportError:
        raise http.Http404

    if not (request.user.is_authenticated() and
            request.user.is_staff):
        raise http.Http404

    # get first memcached URI
    m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
    )
    if not m:
        raise http.Http404

    host = memcache._Host(m.group(1))
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    return render_to_response(
        'memcached_status.html', dict(
            stats=stats,
            hit_rate=100 * stats.get_hits / stats.cmd_get,
            time=datetime.datetime.now(), # server time
        ))
