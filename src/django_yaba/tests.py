import unittest
import datetime
from django.contrib.auth.models import User
from django_yaba import models
from django.test.client import Client

class BlogWebTest(unittest.TestCase):
    """
    YaBa Unit Tests
    """

    def setUp(self):
        self.client = Client()

    def test_frontpage(self):
        response = self.client.get('/')

        self.failUnless(response.status_code, 200)

    def test_rss_feeds(self):
        response = self.client.get('/feeds/rss/')

        self.failUnless(response.status_code, 200)

    def test_gallery(self):
        response = self.client.get('/gallery/list/')

        self.failUnless(response.status_code, 200)

    def test_blog_by_id(self):
        response = self.client.get('/view/1/')

        self.failUnless(response.items()[0][1],
            302)

    def test_blog_by_slug(self):
        response = self.client.get('/pc-gamer-missing-anything/')

        self.failUnless(response.items()[0][1], 200)

class BlogModelTests(unittest.TestCase):
    """
    YaBa Unit Tests
    """

    def setUp(self):
        self.user = User.objects.create(username='test',
            email='test@testing.com'
            )
        self.user.set_password('testing')
        self.category = models.Category.objects.create(
            label="Test Category",
            slug="test-category"
            )
        self.link = models.Links.objects.create(
            label="Test Link",
            slug="test-link",
            site_link="http://www.google.com/"
            )
        self.story = models.Story.objects.create(
            title="Test 1",
            slug="test-1",
            body="Test Blog Post",
            owner=self.user
            )
        self.article = models.Article.objects.create(
            title="Test Article",
            slug="test-article",
            body="Test Article Post",
            owner=self.user,
            buttoned=True
            )

    def test_items(self):
        self.assertEquals(self.story.get_absolute_url(), '/test-1/')
        self.assertEquals(self.article.get_absolute_url(), 
            '/article/test-article/')
