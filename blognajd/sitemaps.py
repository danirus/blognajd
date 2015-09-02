import copy
from datetime import datetime
from django.contrib.sitemaps import Sitemap

from usersettings.shortcuts import get_current_usersettings as sitesettings
from blognajd.models import PUBLIC, Story


ditems = {
    'about': {'loc': '/about', 'priority': 1.0},
    'blog': {'loc': '/blog', 'priority': 1.0},
    'projects': {'loc': '/projects', 'priority': 1.0},
    'contact': {'loc': '/contact/', 'priority': 1.0}
}


class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def __init__(self, *args, **kwargs):
        super(StaticSitemap, self).__init__(*args, **kwargs)
        self.ditems = copy.deepcopy(ditems)

    def items(self):
        if not sitesettings().has_about_page and \
           self.ditems.get('about', False):
            self.ditems.pop('about')
        if not sitesettings().has_projects_page and \
           self.ditems.get('projects', False):
            self.ditems.pop('projects')
        if not sitesettings().has_contact_page and \
           self.ditems.get('contact', False):
            self.ditems.pop('contact')
        return list(self.ditems)

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
