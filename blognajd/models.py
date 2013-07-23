#-*- coding: utf-8 -*-
from datetime import date
import os.path

from django.db import models
from django.db.models import permalink, Q
from django.db.models.signals import post_delete
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
# from django.utils.timezone import now

from django_markup.fields import MarkupField
from django_markup.markup import formatter
from inline_media.fields import TextFieldWithInlines
from inline_media.utils import unescape_inline
from tagging.fields import TagField
from tagging.models import TaggedItem
from tagging.utils import get_tag_list


DRAFT = 1
PUBLIC = 2
STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLIC, "Public"),)


class StoryManager(models.Manager):
    """Returns published posts that are not in the future."""
    
    def drafts(self):
        return self.get_query_set().filter(status=DRAFT).order_by("-pub_date")

    def upcoming(self):
        return self.get_query_set().filter(
            status=PUBLIC, pub_date__gt=date.today()).order_by("-pub_date")

    def published(self):
        return self.get_query_set().filter(
            status=PUBLIC, pub_date__lte=date.today()).order_by("-pub_date")

    def select(self, status=[PUBLIC]):
        return self.get_query_set().filter(
            status__in=status, pub_date__lte=date.today()).order_by("-pub_date")


class Story(models.Model):
    """A generic story."""
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique_for_date="pub_date")
    markup          = MarkupField(default="markdown")
    abstract        = TextFieldWithInlines()
    abstract_markup = models.TextField(editable=True, blank=True, null=True)
    body            = TextFieldWithInlines()
    body_markup     = models.TextField(editable=True, blank=True, null=True)
    tags            = TagField()
    status          = models.IntegerField(choices=STATUS_CHOICES, default=1)
    allow_comments  = models.BooleanField(default=True)
    pub_date        = models.DateField("Publication date", default=date.today())
    mod_date        = models.DateField("Modification date", auto_now=True)
    visits          = models.IntegerField(default=0, editable=False)
    objects         = StoryManager()

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"
        db_table  = "blog_stories"
        ordering  = ("-pub_date",)
        get_latest_by = "pub_date"
        permissions = (("can_see_unpublished_stories", 
                        "Can see unpublished stories"),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.abstract_markup = mark_safe(
            formatter(self.abstract, filter_name=self.markup))
        self.body_markup = mark_safe(
            formatter(self.body, filter_name=self.markup))
        if self.markup == "restructuredtext":
            self.abstract_markup = unescape_inline(self.abstract_markup)
            self.body_markup = unescape_inline(self.body_markup)
        super(Story, self).save(*args, **kwargs)
        if self.status == PUBLIC:
            try:
                ping_google()
            except:
                pass

    @permalink
    def get_absolute_url(self):
        kwargs = { "year": self.pub_date.year,
                   "month": self.pub_date.strftime("%b").lower(),
                   "day": self.pub_date.day,
                   "slug": self.slug }

        if self.status == DRAFT:
            return ("blog-story-detail-draft", None, kwargs)
        elif self.pub_date > date.today():
            return ("blog-story-detail-upcoming", None, kwargs)
        else:
            return ("blog-story-detail", None, kwargs)

    @property
    def in_the_future(self):
        return self.pub_date > date.today()


def delete_story_tags(sender, instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    tags = get_tag_list(instance.tags)
    TaggedItem._default_manager.filter(content_type__pk=ctype.pk,
                                       object_id=instance.pk,
                                       tag__in=tags).delete()
    for tag in tags:
        if not tag.items.count():
            tag.delete()

post_delete.connect(delete_story_tags, sender=Story)
