#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django import db

from flatblocks_xtd.models import FlatBlockXtd
from flatblocks_xtd.templatetags.flatblock_xtd_tags import do_get_flatblock_xtd
from flatblocks_xtd import settings


class BasicTests(TestCase):
    urls = 'flatblocks_xtd.urls'

    def setUp(self):
        self.testblock = FlatBlockXtd.objects.create(
             slug='block',
             header='HEADER',
             content='CONTENT'
        )
        self.admin = User.objects.create_superuser(
            'admin2', 'admin@localhost', 'adminpwd')

    def testURLConf(self):
        # We have to support two different APIs here (1.1 and 1.2)
        def get_tmpl(resp):
            if hasattr(resp, 'template') and isinstance(resp.template, list):
                return resp.template[0]
            elif hasattr(resp, 'templates'):
                return resp.templates[0]
            return resp.template
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name, 
                          'admin/login.html')
        self.client.login(username='admin2', password='adminpwd')
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name, 
                          'flatblocks_xtd/edit.html')

    def testCacheReset(self):
        """
        Tests if FlatBlockXtd.save() resets the cache.
        """
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" 60 %}')
        tpl.render(template.Context({}))
        name = '%sblock' % settings.CACHE_PREFIX
        self.assertNotEqual(None, cache.get(name))
        block = FlatBlockXtd.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()
        self.assertEqual(None, cache.get(name))

    def testSaveForceUpdate(self):
        block = FlatBlockXtd(slug='missing')
        with self.assertRaises(ValueError):
            block.save(force_update=True)

    def testSaveForceInsert(self):
        block = FlatBlockXtd.objects.get(slug='block')
        with self.assertRaises(db.IntegrityError):
            block.save(force_insert=True)

    def testCacheRemoval(self):
        """
        If a block is deleted it should also be removed from the cache.
        """
        block = FlatBlockXtd(slug="test", content="CONTENT")
        block.save()
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "test" 100 %}')
        # We fill the cache by rendering the block
        tpl.render(template.Context({}))
        cache_key = "%stest" % settings.CACHE_PREFIX
        self.assertNotEqual(None, cache.get(cache_key))
        block.delete()
        self.assertEqual(None, cache.get(cache_key))


class TagTests(TestCase):
    def setUp(self):
        self.testblock = FlatBlockXtd.objects.create(
             slug='block',
             header='HEADER',
             content='CONTENT'
        )

    def testLoadingTaglib(self):
        """Tests if the taglib defined in this app can be loaded"""
        tpl = template.Template('{% load flatblock_xtd_tags %}')
        tpl.render(template.Context({}))

    def testExistingPlain(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% plain_flatblock_xtd "block" %}')
        self.assertEqual('CONTENT', tpl.render(template.Context({})).strip())

    def testExistingTemplate(self):
        expected = """<div class="flatblock-xtd block-block">

    <h2 class="title">HEADER</h2>

    <div class="content">CONTENT</div>
</div>
"""
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})))

    def testUsingMissingTemplate(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" using "missing_template.html" %}')
        exception = template.TemplateSyntaxError
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testSyntax(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(None,
                                    template.Token('TOKEN_TEXT',
                                                   'flatblock_xtd "block"'))
        self.assertEqual('block', node.slug)
        self.assertEqual(False, node.evaluated)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" 123 %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(None, 
                                    template.Token('TOKEN_TEXT',
                                                   'flatblock_xtd "block" 123'))
        self.assertEqual('block', node.slug)
        self.assertEqual(False, node.evaluated)
        self.assertEqual(123, node.cache_time)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" '
            'using "flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT',
                                 'flatblock "block" using '
                                 '"flatblocks_xtd/flatblock_xtd.html"'))
        self.assertEqual('block', node.slug)
        self.assertEqual(False, node.evaluated)
        self.assertEqual(0, node.cache_time)
        self.assertEqual("flatblocks_xtd/flatblock_xtd.html", 
                         node.template_name)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" 123 '
            'using "flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT',
                                 'flatblock "block" 123 using '
                                 '"flatblocks_xtd/flatblock_xtd.html"'))
        self.assertEqual('block', node.slug)
        self.assertEqual(False, node.evaluated)
        self.assertEqual(123, node.cache_time)
        self.assertEqual("flatblocks_xtd/flatblock_xtd.html", 
                         node.template_name)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" evaluated %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT', 'flatblock "block" evaluated'))
        self.assertEqual('block', node.slug)
        self.assertEqual(True, node.evaluated)
        self.assertEqual(0, node.cache_time)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" evaluated using '
            '"flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT',
                                 'flatblock "block" evaluated '
                                 'using '
                                 '"flatblocks_xtd/flatblock_xtd.html"'))
        self.assertEqual('block', node.slug)
        self.assertEqual(True, node.evaluated)
        self.assertEqual(0, node.cache_time)
        self.assertEqual("flatblocks_xtd/flatblock_xtd.html", 
                         node.template_name)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" 123 evaluated %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT',
                                 'flatblock "block" 123 '
                                 'evaluated'))
        self.assertEqual(123, node.cache_time)
        self.assertEqual(True, node.evaluated)

        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" 123 evaluated '
            'using "flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))
        node = do_get_flatblock_xtd(
            None, template.Token('TOKEN_TEXT',
                                 'flatblock "block" 123 '
                                 'evaluated using '
                                 '"flatblocks_xtd/flatblock_xtd.html"'))
        self.assertEqual('block', node.slug)
        self.assertEqual(True, node.evaluated)
        self.assertEqual(123, node.cache_time)
        self.assertEqual("flatblocks_xtd/flatblock_xtd.html", 
                         node.template_name)

    def testBlockAsVariable(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd blockvar %}')
        tpl.render(template.Context({'blockvar': 'block'}))

    def testContentEvaluation(self):
        """
        If a block is set in the template to be evaluated the actual content of
        the block is treated as a Django template and receives the parent
        template's context.
        """
        FlatBlockXtd.objects.create(slug='tmpl_block',
                                    header='HEADER',
                                    content='{{ variable }}')
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% plain_flatblock_xtd "tmpl_block" evaluated %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('value', result)

    def testDisabledEvaluation(self):
        """
        If "evaluated" is not passed, no evaluation should take place.
        """
        FlatBlockXtd.objects.create(slug='tmpl_block',
                                    header='HEADER',
                                    content='{{ variable }}')
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% plain_flatblock_xtd "tmpl_block" %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('{{ variable }}', result)

    def testHeaderEvaluation(self):
        """
        Also the header should receive the context and get evaluated.
        """
        FlatBlockXtd.objects.create(slug='tmpl_block',
                                    header='{{ header_variable }}',
                                    content='{{ variable }}')
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "tmpl_block" evaluated %}')
        result = tpl.render(template.Context({
                    'variable': 'value',
                    'header_variable': 'header-value'}))
        self.assertTrue('header-value' in result)


class AutoCreationTest(TestCase):
    """ Test case for block autcreation """

    def testMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name will be auto-created"""
        expected = """<div class="flatblock-xtd block-foo">

    <div class="content">foo</div>
</div>"""
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "foo" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.count(), 1)
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.count(), 1)

    def testNotAutocreatedMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name won't be auto-created if feature is disabled"""
        expected = ""
        settings.AUTOCREATE_STATIC_BLOCKS = False
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.filter(slug='block').count(), 0)

    def testMissingVariableBlock(self):
        """Tests if a missing block with variable name will simply return an empty string"""
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd name %}')
        self.assertEqual('', 
                         tpl.render(template.Context({'name': 'foo'})).strip())
