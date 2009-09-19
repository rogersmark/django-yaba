import unittest
import datetime
from django.test.client import Client

class BlogTest(unittest.TestCase):
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

