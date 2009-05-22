import datetime, markdown
from django.contrib.comments.views import comments
from django_yaba.blog.comments import wrapped_post_comment
from markdown import markdown
from django.db.models import permalink
from django_yaba.blog.fields import ThumbnailImageField
from django.contrib.auth.models import User
from django.db import models

VIEWABLE_STATUS = [3, 4]

class ViewableManager(models.Manager):
    def get_query_set(self):
        default_queryset = super(ViewableManager, self).get_query_set()
        return default_queryset.filter(status__in=VIEWABLE_STATUS)

class Category(models.Model):
    """ Categories for the Content that is Submitted """
    label = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.label
  
    @permalink
    def get_absolute_url(self):
        return ("blog-category", (), {'slug' : self.slug})

class Links(models.Model):
    """ A model for links to other sites """
    label = models.CharField(max_length=100)
    site_link = models.CharField(max_length=300)
    slug = models.SlugField()

    class Meta:
        ordering = ['label']
        verbose_name_plural = "links"

    def __unicode__(self):
        return self.label


class Story(models.Model):
    """ If this model name isn't self explanatory, quit life """

    STATUS_CHOICES = (
        (1, "Needs Edit"),
        (2, "Needs Approval"),
        (3, "Published"),
        (4, "Archived"),
    )

    title = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category)
    markdown_content = models.TextField()
    html_content = models.TextField(editable=False)
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-modified']
        verbose_name_plural = "stories"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("blog-story", (), {'slug' : self.slug})

    def save(self):
        self.html_content = markdown(self.markdown_content)
        self.modified = datetime.datetime.now()
        super(Story, self).save()

    admin_objects = models.Manager()
    objects = ViewableManager()

class Article(models.Model):
    """ Articles are a bit different from Stories. These are 'extra' content pieces. For instance items that don't belong as news, maybe like a projects page of sorts. 
        By setting 'buttoned' to true in the admin panel, the buttons on the top nav bar will link to this page, and the text will be the title of this page
    """

    STATUS_CHOICES = (
        (1, "Needs Edit"),
        (2, "Needs Approval"),
        (3, "Published"),
        (4, "Archived"),
    )

    title = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category)
    markdown_content = models.TextField()
    html_content = models.TextField(editable=False)
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    buttoned = models.BooleanField()
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['modified']
        verbose_name_plural = "articles"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("blog-article", (), {'slug' : self.slug})

    def save(self):
        self.html_content = markdown(self.markdown_content)
        self.modified = datetime.datetime.now()
        super(Article, self).save()

    admin_objects = models.Manager()
    objects = ViewableManager()

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
    item = models.ForeignKey(Item)
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='photos')
    caption = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id' : self.id})

comments.post_comment = wrapped_post_comment
