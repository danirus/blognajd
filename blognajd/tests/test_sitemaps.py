#-*- coding: utf-8 -*-

from mock import patch
from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from blognajd.models import Story
from blognajd.sitemaps import StaticSitemap, StoriesSitemap


class StaticSitemap1TestCase(DjangoTestCase):    
    def setUp(self):
        self.sitemap = StaticSitemap()

    @patch.multiple('blognajd.conf.settings', BLOGNAJD_HAS_ABOUT=False, 
                    BLOGNAJD_HAS_PROJECTS=False, BLOGNAJD_HAS_CONTACT=False)
    def test_staticsitemap_items_disabled(self):
        self.assertEqual([i for i in self.sitemap.items()], ['blog'])

    @patch.multiple('blognajd.conf.settings', BLOGNAJD_HAS_ABOUT=True, 
                    BLOGNAJD_HAS_PROJECTS=True, BLOGNAJD_HAS_CONTACT=True)
    def test_staticsitemap_items_disabled(self):
        self.assertEqual(sorted([i for i in self.sitemap.items()]), 
                         ['about', 'blog', 'contact', 'projects'])

    @patch.multiple('blognajd.conf.settings', BLOGNAJD_HAS_ABOUT=True, 
                    BLOGNAJD_HAS_PROJECTS=True, BLOGNAJD_HAS_CONTACT=True)
    def test_staticsitemap_location(self):
        for item in self.sitemap.items():
            if item == 'contact':
                urlname = 'contactme-get-contact-form'
            else: urlname = item
            self.assertEqual(self.sitemap.location(item), reverse(urlname))


class StoriesSitemapTestCase(DjangoTestCase):
    def test_storiessitemap_empty(self):
        sitemap = StoriesSitemap()
        self.assertEqual(len(sitemap.items()), 0)


class StoriesSitemapTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']

    def setUp(self):
        self.story = Story.objects.get(pk=1)
        self.sitemap = StoriesSitemap()

    def test_storiessitemap_items(self):
        self.assertEqual(len(self.sitemap.items()), 1)

    def test_storiessitemap_lastmod(self):
        for item in self.sitemap.items():
            self.assertEqual(self.sitemap.lastmod(item), self.story.mod_date)
