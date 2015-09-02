from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from blognajd.models import Story, SiteSettings
from blognajd.sitemaps import StaticSitemap, StoriesSitemap


class StaticSitemap1TestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json']

    def test_staticsitemap_items_disabled(self):
        sitesettings = SiteSettings.objects.get(pk=1)
        sitesettings.has_about_page = False
        sitesettings.has_projects_page = False
        sitesettings.has_contact_page = False
        sitesettings.save()
        self.assertEqual([i for i in StaticSitemap().items()], ['blog'])

    def test_staticsitemap_items_enabled(self):
        sitesettings = SiteSettings.objects.get(pk=1)
        sitesettings.has_about_page = True
        sitesettings.has_projects_page = True
        sitesettings.has_contact_page = True
        sitesettings.save()
        self.assertEqual(sorted([i for i in StaticSitemap().items()]),
                         ['about', 'blog', 'contact', 'projects'])

    def test_staticsitemap_location(self):
        sitemap = StaticSitemap()
        for item in sitemap.items():
            if item == 'contact':
                urlname = 'contactme-get-contact-form'
            else:
                urlname = item
            self.assertEqual(sitemap.location(item), reverse(urlname))


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
