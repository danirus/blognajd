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

import copy
import datetime
from mock import patch
import os

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase as DjangoTestCase
from django.test.utils import override_settings

from inline_media.models import License, Picture

from blognajd.models import DRAFT, PUBLIC, Story


STORY_URL_KWARGS = {'year':2013, 'month':'jul', 'day':16, 'slug':'first-story'}

def get_license():
    try:
        return License.objects.get(pk=1)
    except License.DoesNotExist:
        return License.objects.create(
            name="default license",
            link="http://creativecommons.org/licenses/by-sa/3.0/")

def create_picture():
    curdir = os.path.dirname(__file__)
    ifile = os.path.join(curdir, "images/theweb.jpg")
    image = ImageFile(open(ifile, "rb"))
    picture = Picture.objects.create(title="the web", 
                                     description="picture description",
                                     author="picture author",
                                     license=get_license(),
                                     picture=image)
    return picture

class InlineMediaURLTestCase(DjangoTestCase):
    fixtures = ['site_tests.json', 'auth_tests.json']

    def setUp(self):
        self.pic = create_picture()
        logged = self.client.login(username='admin', password='admin')
        self.assertTrue(logged)

    def test_inline_media_url(self):
        url = reverse('inline-media-render-inline',
                      kwargs={'size': 80,
                              'align': 'center',
                              'oid': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(url.startswith("/inline-media"))


class CommentsURLsTestCase(DjangoTestCase):
    def test_django_comments_xtd_urls(self):
        url1 = reverse('comments-xtd-sent')
        self.assertTrue(url1.startswith('/comments/sent/'))
        url2 = reverse('comments-xtd-confirm', kwargs={'key': 'whatever'})
        self.assertTrue(url2.startswith('/comments/confirm/whatever'))
        url3 = reverse('comments-xtd-reply', kwargs={'cid': 1234})
        self.assertTrue(url3.startswith('/comments/reply/1234'))
        
class TagsURLsTestCase(DjangoTestCase):
    def test_tag_urls(self):
        url1 = reverse('tags')
        self.assertTrue(url1.startswith('/tags'))
        url2 = reverse('tag-detail', kwargs={'slug': 'anything'})
        self.assertTrue(url2.startswith('/tag/anything'))

class FeedsURLsTestCase(DjangoTestCase):
    def test_feed_stories(self):
        url1 = reverse('stories-feed')
        self.assertTrue(url1.startswith('/feeds/stories/'))
        url2 = reverse('tag-detail-feed', kwargs={'slug': 'anything'})
        self.assertTrue(url2.startswith('/feeds/tag/anything'))
        
class AdminMenuURLsTestCase(DjangoTestCase):
    def test_admin_menu_option_urls(self):
        url1 = reverse('unpublished-on')
        self.assertTrue(url1.startswith('/unpublished-on/'))
        url2 = reverse('unpublished-off')
        self.assertTrue(url2.startswith('/unpublished-off/'))
       
class BlogHomepageURLTestCase(DjangoTestCase):
    def test_blog_url(self):
        url = reverse('blog')
        self.assertTrue(url.startswith('/blog'))

class ArchiveURLsTestCase(DjangoTestCase):
    def test_archive_redirect(self):
        url1 = reverse('archive')
        self.assertTrue(url1.startswith('/archive'))
        url2 = reverse('archive-year', kwargs={'year': 2013})
        self.assertTrue(url2.startswith('/archive/2013'))

class BlogStoryDetailURLTestCase(DjangoTestCase):
    def test_blog_story_detail_month_numeric_url(self): 
        kwargs = copy.copy(STORY_URL_KWARGS)
        kwargs['month'] = 7
        url = reverse('blog-story-detail-month-numeric', kwargs=kwargs)
        self.assertEqual(url, '/2013/7/16/first-story/')
       
    def test_blog_story_detail_url(self):
        url = reverse('blog-story-detail', kwargs=STORY_URL_KWARGS)
        self.assertEqual(url, '/2013/jul/16/first-story/')
        
class BlogStoryDetailDraft1TestCase(DjangoTestCase):
    def setUp(self):
        self.url = reverse('blog-story-detail-draft', kwargs=STORY_URL_KWARGS)

    def test_blog_story_detail_draft_url(self):
        self.assertEqual(self.url, '/draft/2013/jul/16/first-story/')
        
    def test_blog_story_detail_draft_requires_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('http://testserver/', 302),])

class BlogStoryDetailDraft2TestCase(DjangoTestCase):
    # test decorator 'login_required'
    fixtures = ['auth_tests.json', 'story_tests.json']

    def setUp(self):
        self.url = reverse('blog-story-detail-draft', kwargs=STORY_URL_KWARGS)
        logged = self.client.login(username='admin', password='admin')
        self.assertTrue(logged)
        story = Story.objects.get(pk=1)
        story.status = DRAFT
        story.save()

    def test_story_detail_draft_after_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.templates[0].name, 
                         'blognajd/story_detail.html')
        self.assertEqual(response.templates[1].name, 'blognajd/base.html')

class BlogStoryDetailDraft3TestCase(DjangoTestCase):
    # test decorator 'permission_required'
    fixtures = ['auth_tests.json', 'story_tests.json']

    def setUp(self):
        self.url = reverse('blog-story-detail-draft', kwargs=STORY_URL_KWARGS)
        bob = User.objects.create_user("bob", "bob@example.com", "admin")
        alice = User.objects.create_user("alice", "alice@example.com", "admin")
        # setup permission for alice
        ct_story = ContentType.objects.get(app_label="blognajd", model="story")
        permission = Permission.objects.get(
            content_type=ct_story, codename="can_see_unpublished_stories")
        alice.user_permissions.add(permission)
        alice.save()
        self.assertTrue(alice.has_perm("blognajd.can_see_unpublished_stories"))
        # change story status
        story = Story.objects.get(pk=1)
        story.status = DRAFT
        story.save()

    def test_story_detail_draft_without_permissions(self):
        logged = self.client.login(username='bob', password='admin')
        self.assertTrue(logged)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        redirected = ('http://testserver/?next={0}'.format(self.url), 302)
        self.assertEqual(response.redirect_chain, [redirected])
        self.assertEqual(response.templates[0].name, 'blognajd/index.html')
        
    def test_story_detail_draft_with_permissions(self):
        logged = self.client.login(username='alice', password='admin')
        self.assertTrue(logged)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.templates[0].name, 
                         'blognajd/story_detail.html')

class BlogStoryDetailUpcoming1TestCase(DjangoTestCase):
    def setUp(self):
        self.url = reverse('blog-story-detail-upcoming', 
                           kwargs=STORY_URL_KWARGS)

    def test_blog_story_detail_draft_url(self):
        self.assertEqual(self.url, '/upcoming/2013/jul/16/first-story/')
        
    def test_blog_story_detail_draft_requires_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('http://testserver/', 302),])

class BlogStoryDetailUpcoming2TestCase(DjangoTestCase):
    # test decorator 'login_required'
    fixtures = ['auth_tests.json', 'story_tests.json']

    def setUp(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        kwargs = { 'year': tomorrow.year,
                   'month': tomorrow.strftime("%b").lower(),
                   'day': tomorrow.day,
                   'slug': STORY_URL_KWARGS['slug'] }
        self.url = reverse('blog-story-detail-upcoming', kwargs=kwargs)
        logged = self.client.login(username='admin', password='admin')
        self.assertTrue(logged)
        story = Story.objects.get(pk=1)
        # change story pub_date to make an upcoming story
        story.pub_date = tomorrow
        story.save()

    def test_story_detail_upcoming_after_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.templates[0].name, 
                         'blognajd/story_detail.html')
        self.assertEqual(response.templates[1].name, 'blognajd/base.html')

class BlogStoryDetailUpcoming3TestCase(DjangoTestCase):
    # test decorator 'permission_required'
    fixtures = ['auth_tests.json', 'story_tests.json']

    def setUp(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        kwargs = { 'year': tomorrow.year,
                   'month': tomorrow.strftime("%b").lower(),
                   'day': tomorrow.day,
                   'slug': STORY_URL_KWARGS['slug'] }
        self.url = reverse('blog-story-detail-upcoming', kwargs=kwargs)
        bob = User.objects.create_user("bob", "bob@example.com", "admin")
        alice = User.objects.create_user("alice", "alice@example.com", "admin")
        # setup permission for alice
        ct_story = ContentType.objects.get(app_label="blognajd", model="story")
        permission = Permission.objects.get(
            content_type=ct_story, codename="can_see_unpublished_stories")
        alice.user_permissions.add(permission)
        alice.save()
        self.assertTrue(alice.has_perm("blognajd.can_see_unpublished_stories"))
        # change story pub_date to make an upcoming story
        story = Story.objects.get(pk=1)
        story.pub_date = tomorrow
        story.save()

    def test_story_detail_upcoming_without_permissions(self):
        logged = self.client.login(username='bob', password='admin')
        self.assertTrue(logged)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        redirected = ('http://testserver/?next={0}'.format(self.url), 302)
        self.assertEqual(response.redirect_chain, [redirected])
        self.assertEqual(response.templates[0].name, 'blognajd/index.html')
        
    def test_story_detail_upcoming_with_permissions(self):
        logged = self.client.login(username='alice', password='admin')
        self.assertTrue(logged)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.templates[0].name, 
                         'blognajd/story_detail.html')

class SitemapURLTestCase(DjangoTestCase):
    def test_sitemap_url(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        
    # Skip due to django 1.5.1 bug under python 3
    # def test_sitemap_static_url(self): 
    #     response = self.client.get('/sitemap-static.xml')
    #     self.assertEqual(response.status_code, 200)

    def test_sitemap_stories_url(self): 
        response = self.client.get('/sitemap-stories.xml')
        self.assertEqual(response.status_code, 200)
       
class AboutURLTestCase(DjangoTestCase):
    def test_about_url_enabled(self):
        url = reverse('about')
        self.assertEqual(url, '/about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'blognajd/about.html')
        self.assertEqual(response.templates[1].name, 'blognajd/base.html')

class ProjectsURLTestCase(DjangoTestCase):
    def test_projects_url(self):
        url = reverse('projects')
        self.assertEqual(url, '/projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'blognajd/projects.html')
        self.assertEqual(response.templates[1].name, 'blognajd/base.html')

class ContactmeURLsTestCase(DjangoTestCase):
    def test_django_contactme_urls(self):
        url1 = reverse('contactme-get-contact-form')
        self.assertTrue(url1.startswith('/contact/'))
        url2 = reverse('contactme-post-contact-form')
        self.assertTrue(url2.startswith('/contact/post/'))
        url3 = reverse('contactme-confirm-contact', kwargs={'key': 1234})
        self.assertTrue(url3.startswith('/contact/confirm/1234'))
