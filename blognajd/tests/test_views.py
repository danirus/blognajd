from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from taggit.models import Tag, TaggedItem
from usersettings.shortcuts import get_current_usersettings as sitesettings

from blognajd.models import DRAFT, PUBLIC, Story
from blognajd.views import HomepageView, TagDetailView


class UnpublishedTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json', 'auth_tests.json']

    def test_show_unpublised_requires_login(self):
        self.client.get(reverse('unpublished-on'))
        self.assertEqual(self.client.session.get('unpublished_on', None), None)
        self.client.get(reverse('unpublished-off'))
        self.assertEqual(self.client.session.get('unpublished_on', None), None)

    def test_show_unpublished_in_session(self):
        logged = self.client.login(username='admin', password='admin')
        self.assertTrue(logged)
        self.client.get(reverse('unpublished-on'), follow=True)
        self.assertTrue(self.client.session['unpublished_on'])
        self.client.get(reverse('unpublished-off'), follow=True)
        self.assertFalse(self.client.session['unpublished_on'])


class StoryListViewTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json']

    def test_admin_menu_option_urls(self):
        response = self.client.get(reverse('blog'))
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.templates[0].name, 'blognajd/blog.html')
        self.assertTrue(response.templates[1].name, 'blognajd/base.html')


class ArchiveRedirectViewTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json']

    def test_archive_view_redirect_home(self):
        response = self.client.get(reverse('archive'), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('http://testserver/', 302), ])
        self.assertTrue(response.templates[0].name, 'blognajd/index.html')
        self.assertTrue(response.templates[1].name, 'blognajd/base.html')

    def test_archive_year_view_with_empty_db(self):
        response = self.client.get(
            reverse('archive-year', kwargs={'year': 2013}),
            follow=True)
        self.assertTrue(response.status_code, 404)
        self.assertTrue(response.templates[0].name, 'blognajd/404.html')


class StoryDetailViewTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json', 'story_tests.json']

    def test_blog_story_detail_month_numeric(self):
        url = reverse('blog-story-detail-month-numeric',
                      kwargs={'year': 2013,
                              'month': 7,
                              'day': 16,
                              'slug': 'first-story'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                         'blognajd/story_detail.html')
        self.assertEqual(response.templates[1].name,
                         'blognajd/base.html')

    def test_blog_story_detail(self):
        url = reverse('blog-story-detail',
                      kwargs={'year': 2013,
                              'month': 'jul',
                              'day': 16,
                              'slug': 'first-story'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                         'blognajd/story_detail.html')
        self.assertEqual(response.templates[1].name,
                         'blognajd/base.html')


class HomepageViewTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json',
                'auth_tests.json',
                'story_tests.json']

    def test_homepageview_queryset_unpublished_off(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blognajd/index.html')
        self.assertEqual(list(response.context['object_list']),
                         list(Story.objects.select([PUBLIC])
                              .order_by('-pub_date')))

    def test_homepageview_queryset_unpublished_on(self):
        self.client.login(username="admin", password="admin")
        self.client.get(reverse('unpublished-on'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blognajd/index.html')
        self.assertEqual(list(response.context['object_list']),
                         list(Story.objects.select([DRAFT, PUBLIC])
                              .order_by('-pub_date')))

    def test_homepageview_get_paginate_by(self):
        self.assertEqual(HomepageView().get_paginate_by(None),
                         sitesettings().paginate_by)


class TagDetailViewTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json', 'story_tests.json']

    def test_tagdetailview_queryset(self):
        story = Story.objects.get(pk=1)
        story.tags.add('something')
        response = self.client.get(reverse('tag-detail',
                                           kwargs={'slug': 'something'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blognajd/tag_detail.html')
        taggeditems = TaggedItem.objects.filter(tag__name__iexact='something')
        self.assertEqual(response.context['object_list'][0],
                         taggeditems[0].content_object)
        self.assertEqual(response.context['object'],
                         Tag.objects.filter(name='something')[0])

    def test_tagdetailview_get_paginate_by(self):
        self.assertEqual(TagDetailView().get_paginate_by(None),
                         sitesettings().paginate_by)
