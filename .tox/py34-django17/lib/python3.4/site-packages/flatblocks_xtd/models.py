#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from flatblocks_xtd.settings import CACHE_PREFIX
from inline_media.fields import TextFieldWithInlines


@python_2_unicode_compatible
class FlatBlockXtd(models.Model):
    """
    Think of a flatblock_xtd as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(max_length=255, unique=True,
                            verbose_name=_('Slug'),
                            help_text=_("A unique name used for reference "
                                        "in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                              verbose_name=_('Header'),
                              help_text=_("An optional header for "
                                          "this content"))
    content = TextFieldWithInlines(_('Content'), blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        super(FlatBlockXtd, self).save(*args, **kwargs)
        # Now also invalidate the cache used in the templatetag
        cache.delete('%s%s' % (CACHE_PREFIX, self.slug, ))

    def delete(self, *args, **kwargs):
        cache_key = '%s%s' % (CACHE_PREFIX, self.slug,)
        super(FlatBlockXtd, self).delete(*args, **kwargs)
        cache.delete(cache_key)

    class Meta:
        verbose_name = _('Flat block with inline media')
        verbose_name_plural = _('Flat blocks with inline media')
