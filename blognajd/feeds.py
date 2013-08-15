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

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse

from inline_media.parser import inlines
from tagging.models import Tag, TaggedItem

from blognajd.conf import settings
from blognajd.models import Story


# ct_story = ContentType.objects.get(app_label="blognajd", model="story")


class LatestStoriesFeed(Feed):
    
    def item_pubdate(self, item):
        return datetime.datetime(item.pub_date.year,
                                 item.pub_date.month,
                                 item.pub_date.day, 0, 0, 0)

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return inlines(item.body)

    def item_author_name(self, item):
        return settings.BLOGNAJD_META_AUTHOR

    def title(self):
        return '{0} stories feed'.format(
            settings.BLOGNAJD_SITE_SHORT_NAME)

    def description(self):
        return '{0} latest stories feed.'.format(
            settings.BLOGNAJD_SITE_LONG_NAME)

    def link(self):
        return reverse('blog')

    def items(self):
        return Story.objects.published()[:10]


class StoriesByTag(Feed):

    def get_object(self, request, slug):
        if not slug:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=slug)

    def title(self, obj):
        return r'''{0} posts tagged as '{1}' feed'''.format(
            settings.BLOGNAJD_SITE_SHORT_NAME, obj.name)

    def description(self):
        return r'''{0} latest posts tagged as '{1}' feed.'''.format(
            settings.BLOGNAJD_SITE_SHORT_NAME, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('tag-detail-feed', kwargs={"slug": obj.name})

    def feed_url(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('tag-detail-feed', kwargs={"slug": obj.name})

    def description(self, obj):
        return "Posts tagged as %s" % obj.name
    
    def items(self, obj):
        ct_story = ContentType.objects.get(app_label="blognajd", model="story")
        return TaggedItem.objects.filter(
            tag__name__iexact=obj.name,
            content_type__in=[ct_story,]).order_by("-id")[:10]

    def item_pubdate(self, item):
        return datetime.datetime(item.object.pub_date.year,
                                 item.object.pub_date.month,
                                 item.object.pub_date.day, 0, 0, 0)

    def item_title(self, item):
        return item.object.title

    def item_link(self, item):
        return item.object.get_absolute_url()

    def item_description(self, item):
        return inlines(item.object.body)

    def item_author_name(self, item):
        return settings.BLOGNAJD_META_AUTHOR
