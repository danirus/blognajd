#-*- coding: utf-8 -*-

import lxml
import urllib

from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from tagging.models import Tag

from blognajd.conf import settings
from blognajd.feeds import LatestStoriesFeed, StoriesByTag
from blognajd.models import Story

class LatestStoriesFeedTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']

    def setUp(self):
        response = self.client.get(reverse('stories-feed'))
        tree = lxml.etree.fromstring(response.content)
        self.assert_(len(tree.getchildren()) == 1)
        self.channel = tree.find('channel')
        self.feed = LatestStoriesFeed()

    def test_stories_feed_title(self):
        self.assertEqual(self.channel.find('title').text, self.feed.title())

    def test_stories_feed_link(self):
        url = urllib.parse.urlparse(self.channel.find('link').text)
        self.assertEqual(url.path, self.feed.link())

    def test_stories_feed_description(self):
        self.assertEqual(self.channel.find('description').text, 
                         self.feed.description())

    def test_stories_feed_atom_link(self):
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        atomlink_list = self.channel.xpath('atom:link', namespaces=namespaces)
        self.assert_(len(atomlink_list) == 1)
        atomlink = atomlink_list.pop()
        for attrib_key in ['href', 'rel']:
            self.assert_(attrib_key in atomlink.attrib.keys())
        # read the url from the attribute and parse it to compare only the path
        url = urllib.parse.urlparse(atomlink.attrib['href'])
        self.assertEqual(url.path, reverse('stories-feed'))
   
    def test_stories_feed_items(self):
        self.assert_(len(self.channel.findall('item')) == 1)
        item = self.channel.findall('item')[0]
        story = Story.objects.get(pk=1)
        self.assertEqual(item.find('title').text, story.title)
        url = urllib.parse.urlparse(item.find('link').text)
        self.assertEqual(url.path, story.get_absolute_url())
        namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}
        creator_list = item.xpath('dc:creator', namespaces=namespaces)
        self.assert_(len(creator_list) == 1)
        creator = creator_list.pop()
        self.assertEqual(creator.text, settings.BLOGNAJD_META_AUTHOR)
        self.assert_(len(item.find('pubDate')) != None)
        self.assert_(len(item.find('guid')) != None)


class StoriesByTagFeedTestCase(DjangoTestCase):
    fixtures = ['story_tests.json']

    def setUp(self):
        self.tagname = 'something'
        story = Story.objects.get(pk=1)
        story.tags = self.tagname
        story.save()
        response = self.client.get(reverse('tag-detail-feed', 
                                           kwargs={'slug': self.tagname}))
        tree = lxml.etree.fromstring(response.content)
        self.assert_(len(tree.getchildren()) == 1)
        self.channel = tree.find('channel')
        self.feed = StoriesByTag()
        self.tag = Tag.objects.filter(name=self.tagname)[0]
        self.assertEqual(self.tag.name, self.tagname)

    def test_storiesbytag_feed_get_object(self):
        self.assertEqual(self.feed.get_object(None, self.tagname), self.tag)

    def test_storiesbytag_feed_title(self):
        self.assertEqual(self.channel.find('title').text, 
                         self.feed.title(self.tag))
        
    def test_storiesbytag_feed_link(self):
        url = urllib.parse.urlparse(self.channel.find('link').text)
        self.assertEqual(url.path, self.feed.link(self.tag))
    
    def test_storiesbytag_feed_description(self):
        self.assertEqual(self.channel.find('description').text, 
                         self.feed.description(self.tag))

    def test_storiesbytag_feed_atom_link(self):
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        atomlink_list = self.channel.xpath('atom:link', namespaces=namespaces)
        self.assert_(len(atomlink_list) == 1)
        atomlink = atomlink_list.pop()
        for attrib_key in ['href', 'rel']:
            self.assert_(attrib_key in atomlink.attrib.keys())
        # read the url from the attribute and parse it to compare only the path
        url = urllib.parse.urlparse(atomlink.attrib['href'])
        self.assertEqual(url.path, reverse('tag-detail-feed', 
                                           kwargs={'slug': self.tagname}))

    def test_storiesbytag_feed_items(self):
        self.assert_(len(self.channel.findall('item')) == 1)
        item = self.channel.findall('item')[0]
        story = Story.objects.get(pk=1)
        self.assertEqual(item.find('title').text, story.title)
        url = urllib.parse.urlparse(item.find('link').text)
        self.assertEqual(url.path, story.get_absolute_url())
        namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}
        creator_list = item.xpath('dc:creator', namespaces=namespaces)
        self.assert_(len(creator_list) == 1)
        creator = creator_list.pop()
        self.assertEqual(creator.text, settings.BLOGNAJD_META_AUTHOR)
        self.assert_(len(item.find('pubDate')) != None)
        self.assert_(len(item.find('guid')) != None)
