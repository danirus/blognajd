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
import copy
from mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase
from tagging.models import Tag
from blognajd.models import DRAFT, PUBLIC, Story


STORY_URL_KWARGS = {'year':2013, 'month':'jul', 'day':16, 'slug':'first-story'}

class StoryManagerTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']

    def setUp(self):
        self.story = Story.objects.get(pk=1)

    def test_storymanager_drafts(self):
        self.story.status = DRAFT
        self.story.save()
        drafts = Story.objects.drafts()
        self.assert_(len(drafts) == 1)
        self.assertEqual(drafts[0], self.story)

    @patch('blognajd.models.ping_google')
    def test_storymanager_upcoming(self, fake_ping):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.story.pub_date = tomorrow
        self.story.save()
        upcoming = Story.objects.upcoming()
        self.assert_(len(upcoming) == 1)
        self.assertEqual(upcoming[0], self.story)

    def test_storymanager_published(self):
        published = Story.objects.published()
        self.assert_(len(published) == 1)
        self.assertEqual(published[0], self.story)

    def test_storymanager_select(self): 
        published = Story.objects.select()
        self.assert_(len(published) == 1)
        self.assertEqual(published[0], self.story)
        self.story.status = DRAFT
        self.story.save()
        drafts = Story.objects.select(status=[DRAFT])
        self.assert_(len(drafts) == 1)
        self.assertEqual(drafts[0], self.story)
       
class StoryModelTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']

    def setUp(self):
        self.story = Story.objects.get(pk=1)

    def test_story_str(self):
        self.assertEqual("{0}".format(self.story), self.story.title)

    @patch('blognajd.models.ping_google')
    def test_story_save_populates_markup_fields(self, fake_ping):
        self.story.markup = "markdown"
        self.story.abstract = "[example link](http://example.com)"
        self.story.abstract_markup = ""
        self.story.body = "# header type H1"
        self.story.body_markup = ""
        self.story.save()
        self.assertEqual(self.story.abstract_markup,
                         '<p><a href="http://example.com">example link</a></p>')
        self.assertEqual(self.story.body_markup,
                         '<h1>header type H1</h1>')

    @patch('blognajd.models.ping_google')
    def test_story_save_unescape_inlines_from_restructuredtext(self, fakef):
        text = '\n<inline attr1="foo" attr2="bar">Es war einmal...\n'
        self.story.abstract = text
        self.story.body = text
        self.story.save()
        self.assertEqual(self.story.abstract_markup,
                         ('<p><inline attr1="foo" attr2="bar">'
                          'Es war einmal...</p>\n').strip())
        self.assertEqual(self.story.body_markup,
                         ('<p><inline attr1="foo" attr2="bar">'
                          'Es war einmal...</p>\n').strip())

    @patch('blognajd.models.ping_google')
    def test_story_save_with_public_status_ping_google(self, fake_ping):
        self.assertEqual(self.story.status, PUBLIC)
        self.story.save()
        self.assertTrue(fake_ping.called)

    @patch('blognajd.models.ping_google')
    def test_story_get_absolute_url(self, fake_ping):
        # published
        self.assertEqual(self.story.get_absolute_url(),
                         reverse('blog-story-detail', 
                                 kwargs=STORY_URL_KWARGS))
        # draft
        self.story.status = DRAFT
        self.story.save()
        self.assertEqual(self.story.get_absolute_url(),
                         reverse('blog-story-detail-draft', 
                                 kwargs=STORY_URL_KWARGS))
        # upcoming
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.story.pub_date = tomorrow
        self.story.status = PUBLIC
        self.story.save()
        kwargs = copy.copy(STORY_URL_KWARGS)
        kwargs.update({'year': tomorrow.year, 
                       'month':tomorrow.strftime("%b").lower(),
                       'day': tomorrow.day})
        self.assertEqual(self.story.get_absolute_url(),
                         reverse('blog-story-detail-upcoming', 
                                 kwargs=kwargs))

    def test_story_in_future(self):
        self.assertFalse(self.story.in_the_future)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.story.pub_date = tomorrow
        self.story.save()
        self.assertTrue(self.story.in_the_future)

class DeleteStoryTagsTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']
    
    def setUp(self):
        self.tagname = 'something'
        self.story = Story.objects.get(pk=1)
        self.story.tags = self.tagname
        self.story.save()

    def test_delete_story_tags(self):
        self.assert_(Tag.objects.filter(name=self.tagname).count() == 1)
        self.story.delete()
        self.assert_(Tag.objects.filter(name=self.tagname).count() == 0)

