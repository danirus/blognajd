#-*- coding: utf-8 -*-

# Blognajd,
# Copyright (C) 2013, Daniel Rus Morales

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import include, patterns, url

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import (DetailView, ListView, TemplateView, 
                                  DateDetailView)

from tagging.models import Tag

from blognajd import views
from blognajd.conf import settings
from blognajd.models import Story
from blognajd.feeds import LatestStoriesFeed, StoriesByTag
from blognajd.sitemaps import StaticSitemap, StoriesSitemap

sitemaps = {
    'static': StaticSitemap,
    'stories': StoriesSitemap,
}

handler403 = 'blognajd.views.http403_handler' # permission denied
handler404 = 'blognajd.views.http404_handler' # page not found
handler500 = 'blognajd.views.http500_handler' # server error

urlpatterns = patterns(
    "",
    url(r'^inline-media/', include('inline_media.urls')),
    url(r"^comments/",     include("django_comments_xtd.urls")),
        
    url(r"^tags$",
        TemplateView.as_view(template_name="blognajd/tag_list.html"),
        name="tags"),

    url(r"^tag/(?P<slug>.{1,50})$",
        views.TagDetailView.as_view(),
        name="tag-detail"),

    url(r'^feeds/stories/$', LatestStoriesFeed(), name='stories-feed'),
    url(r"^feeds/tag/(?P<slug>.{1,50})$", StoriesByTag(), 
        name='tag-detail-feed'),

    url(r"^unpublished-on/$", views.show_unpublished, name="unpublished-on"),
    url(r"^unpublished-off/$", views.hide_unpublished, name="unpublished-off"),

    url(r'^blog$', views.StoryListView.as_view(
            model=Story, paginate_by=settings.BLOGNAJD_PAGINATE_BY,
            template_name="blognajd/blog.html"), 
        name='blog'),

    url(r'archive/(?P<year>\d{4})$', views.ArchiveView.as_view(model=Story),
        name='archive-year'),

    url(r'archive$', views.ArchiveRedirectView.as_view(), name='archive'),

    url((r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/'
         r'(?P<slug>[-\w]+)/$'),
        views.StoryDetailView.as_view(
            model=Story, date_field="pub_date", month_format="%m", 
            template_name="blognajd/story_detail.html"),
        name='blog-story-detail-month-numeric'),

    url((r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/'
         r'(?P<slug>[-\w]+)/$'),
        views.StoryDetailView.as_view(
            model=Story, date_field="pub_date", month_format="%b", 
            template_name="blognajd/story_detail.html"),
        name='blog-story-detail'),

    # allowing access to a story in draft mode
    url((r'^draft/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/'
         r'(?P<slug>[-\w]+)/$'),
        login_required(
            permission_required('blognajd.can_see_unpublished_stories')(
                DateDetailView.as_view(
                    queryset=Story.objects.drafts(),
                    date_field="pub_date", month_format="%b", 
                    template_name="blognajd/story_detail.html", 
                    allow_future=True)
                ),
            redirect_field_name=""),
        name='blog-story-detail-draft'),

    # allowing access to an upcoming storie
    url((r'^upcoming/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/'
         r'(?P<slug>[-\w]+)/$'),
        login_required(
            permission_required('blognajd.can_see_unpublished_stories')(
                DateDetailView.as_view(
                    queryset=Story.objects.upcoming(),
                    date_field="pub_date", month_format="%b", 
                    template_name="blognajd/story_detail.html", 
                    allow_future=True)
                ),
                redirect_field_name=""),
        name='blog-story-detail-upcoming'),

    url(r"^$", views.HomepageView.as_view(), name="index"),
)

urlpatterns += patterns("django.contrib.sitemaps.views",
    url(r'^sitemap\.xml$',                 'index',   {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

if settings.BLOGNAJD_HAS_ABOUT:
    urlpatterns += patterns(
        "",
        url(r'^about$', 
            TemplateView.as_view(template_name="blognajd/about.html"), 
            name='about'),
    )

if settings.BLOGNAJD_HAS_PROJECTS:
    urlpatterns += patterns(
        "",
        url(r'^projects$', 
            TemplateView.as_view(template_name="blognajd/projects.html"), 
            name='projects'),
    )

if settings.BLOGNAJD_HAS_CONTACT:
    urlpatterns += patterns(
        "",
        url(r'^contact/', include('django_contactme.urls')),
    )
