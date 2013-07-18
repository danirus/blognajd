#-*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.sitemaps import Sitemap

from blognajd.conf import settings
from blognajd.models import PUBLIC, Story

class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    ditems = {
        'about':    { 'loc':'/about', 'priority':1.0 },
        'blog':     { 'loc':'/blog', 'priority':1.0 },
        'projects': { 'loc':'/projects', 'priority':1.0 },
        'contact':  { 'loc':'/contact/', 'priority':1.0 },
    }

    def items(self):
        if (not settings.BLOGNAJD_HAS_ABOUT and 
            self.ditems.get('about', False)):
            self.ditems.pop('about')
        if (not settings.BLOGNAJD_HAS_PROJECTS and 
            self.ditems.get('projects', False)):
            self.ditems.pop('projects')
        if (not settings.BLOGNAJD_HAS_CONTACT and 
            self.ditems.get('contact', False)):
            self.ditems.pop('contact')
        return self.ditems.keys()
    
    def location(self, obj):
        return self.ditems[obj]['loc']

    def priority(self, obj):
        return self.ditems[obj]['priority']

    def lastmod(self, obj):
        return datetime(
            datetime.today().year, datetime.today().month, 1
            )

class StoriesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Story.objects.filter(
            status__gte=PUBLIC, 
            pub_date__lte=datetime.now()).order_by("-pub_date")

    def lastmod(self, obj):
        return obj.mod_date
