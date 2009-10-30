import datetime, urllib, re, twitter
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.comments.moderation import CommentModerator, moderator
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.db.models import permalink
from django_yaba.fields import ThumbnailImageField
from django.contrib.auth.models import User
from django.db import models

VIEWABLE_STATUS = [3, 4]

class ViewableManager(models.Manager):
    def get_query_set(self):
        default_queryset = super(ViewableManager, self).get_query_set()
        return default_queryset.filter(status__in=VIEWABLE_STATUS)

class Theme(models.Model):
    """
    Users will currently need to upload their own themes to /media/themes/ 
    and then add them via the admin panel
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField()
     
    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Configuration(models.Model):
    """
    General configuration stuff via the admin panel. Currently just handles 
    themes
    """
    title = models.CharField(max_length=50, default="Main Site")
    slug = models.SlugField(default="main-site")
    theme = models.ForeignKey(Theme)

    def __unicode__(self):
        return self.title

class Category(models.Model):
    """
    Categories for the Content that is Submitted
    """
    label = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()

    class Meta:
        ordering = ['label']
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.label
  
    @permalink
    def get_absolute_url(self):
        return ("blog-category", (), {'slug' : self.slug})

class Links(models.Model):
    """
    A model for links to other sites
    """
    label = models.CharField(max_length=100)
    site_link = models.CharField(max_length=300)
    slug = models.SlugField()

    class Meta:
        ordering = ['label']
        verbose_name_plural = "links"

    def __unicode__(self):
        return self.label


class Story(models.Model):
    """
    Status Choices dictate whether or not an article can be seen by the general
    public. Only Published and Archived will be displayed.
    """

    STATUS_CHOICES = (
        (1, "Needs Edit"),
        (2, "Needs Approval"),
        (3, "Published"),
        (4, "Archived"),
    )

    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ManyToManyField(Category)
    body = models.TextField()
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)
    tweet_this = models.BooleanField()
    enable_comments = models.BooleanField(default=True)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self) 

    class Meta:
        ordering = ['-modified']
        verbose_name_plural = "stories"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("blog-story", (), {'slug' : self.slug})

    admin_objects = models.Manager()
    objects = ViewableManager()

class Article(models.Model):
    """ 
    Articles are a bit different from Stories. These are 'extra' content 
    pieces. For instance items that don't belong as news, maybe like a 
    projects page of sorts. 

    By setting 'buttoned' to true in the admin panel, the buttons on the top 
    nav bar will link to this page, and the text will be the title of this page
    """

    STATUS_CHOICES = (
        (1, "Needs Edit"),
        (2, "Needs Approval"),
        (3, "Published"),
        (4, "Archived"),
    )

    title = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()
    category = models.ManyToManyField(Category)
    body = models.TextField()
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    buttoned = models.BooleanField()
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)
    tweet_this = models.BooleanField()
    enable_comments = models.BooleanField(default=True)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    class Meta:
        ordering = ['modified']
        verbose_name_plural = "articles"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("blog-article", (), {'slug' : self.slug})

    admin_objects = models.Manager()
    objects = ViewableManager()

class Gallery(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField()
    owner = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    enable_comments = models.BooleanField(default=True)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "galleries"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("blog-gallery", (), {'slug': self.slug})

class Item(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('item_detail', None, {'object_id' : self.id})

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='gallery/photos')
    caption = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id' : self.id})

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):

    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))

    return content

def post_tweet(sender, instance, created, **kwargs):
    if created:
        if instance.tweet_this:
            try:
                if settings.TWITTER_USERNAME and settings.TWITTER_PASSWORD:
                    url = content_tiny_url("%s/%s" % (settings.ROOT_BLOG_URL,
                        instance.get_absolute_url()))
                    api = twitter.Api(username = settings.TWITTER_USERNAME, 
                        password = settings.TWITTER_PASSWORD)
                    api.PostUpdate("New blog post - %s" % url)
            except:
                pass

def config_name(sender, instance, created, **kwargs):
    if created:
        temp = Configuration.objects.all()
        if temp.count() > 2:
            raise Exception(
                "There can only be one configuration entry, \
                thus only one theme. Sorry!")     

class PostModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'

moderator.register(Story, PostModerator)
moderator.register(Article, PostModerator)
moderator.register(Gallery, PostModerator)

post_save.connect(config_name, sender=Configuration)
post_save.connect(post_tweet, sender=Article)
post_save.connect(post_tweet, sender=Story)
