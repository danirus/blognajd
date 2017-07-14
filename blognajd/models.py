from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.db.models import fields, permalink
from django.db.models.signals import post_delete
from django.contrib.sitemaps import ping_google
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from usersettings.shortcuts import get_current_usersettings

from taggit.managers import TaggableManager
from django_markup.fields import MarkupField
from django_markup.markup import formatter
from inline_media.fields import TextFieldWithInlines
from inline_media.utils import unescape_inline
from usersettings.models import UserSettings


# ----------------------------------------------------------------------
# Web Customizable Site Settings (based on django-usersettings2)
class SiteSettings(UserSettings):
    site_short_name = models.CharField(_('Site short name'), max_length=48,
                                       default='sitename',
                                       help_text='short_short_name')
    site_long_name = models.CharField(_('Site long name'), max_length=256,
                                      default='longname', blank=True,
                                      help_text='site_long_name')
    meta_author = models.CharField(_('Meta author'), max_length=48, blank=True,
                                   default='meta author',
                                   help_text='meta_author')
    meta_keywords = models.CharField(_('Meta keywords'), max_length=256,
                                     default='meta keywords', blank=True,
                                     help_text='meta_keywords')
    meta_description = models.TextField(_('Long description of the site'),
                                        help_text='meta_description',
                                        default='meta description',
                                        blank=True)
    theme = models.CharField(_('Theme'), max_length=24, default='default',
                             help_text='theme')
    paginate_by = models.PositiveSmallIntegerField(
        _('Paginate by'), default=10,
        help_text=_('Number of stories per page (paginate_by)'))
    truncate_to = models.PositiveSmallIntegerField(
        _('Truncate to'), default=200,
        help_text=_(("number of words stories' abstracts get "
                     "truncated to (truncate_to)")))
    has_about_page = models.BooleanField(default=True,
                                         help_text=('has_about_page'))
    has_projects_page = models.BooleanField(default=True,
                                            help_text='has_projects_page')
    has_contact_page = models.BooleanField(default=True,
                                           help_text='has_contact_page')

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'


def get_site_setting(param):
    try:
        sitesettings = get_current_usersettings()
        return getattr(sitesettings, param)
    except AttributeError:
        field, _, _, _ = SiteSettings._meta.get_field_by_name(param)
        if field.default == fields.NOT_PROVIDED:
            return None
        else:
            return field.default


class DefaultSiteSettings:
    def __getattribute__(self, name):
        return get_site_setting(name)

# ----------------------------------------------------------------------

DRAFT = 1
PUBLIC = 2
STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLIC, "Public"),)


class StoryManager(models.Manager):
    """Returns published posts that are not in the future."""

    def drafts(self):
        return self.get_queryset().filter(status=DRAFT).order_by("-pub_date")

    def upcoming(self):
        return self.get_queryset().filter(
            status=PUBLIC, pub_date__gt=date.today()).order_by("-pub_date")

    def published(self):
        return self.get_queryset().filter(
            status=PUBLIC, pub_date__lte=date.today()).order_by("-pub_date")

    def select(self, status=[PUBLIC]):
        return self.get_queryset().filter(
            status__in=status, pub_date__lte=date.today()).order_by("-pub_date")


class Story(models.Model):
    """A generic story."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date="pub_date")
    markup = MarkupField(default="markdown")
    abstract = TextFieldWithInlines()
    abstract_markup = models.TextField(editable=True, blank=True, null=True)
    body = TextFieldWithInlines()
    body_markup = models.TextField(editable=True, blank=True, null=True)
    tags = TaggableManager()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    allow_comments = models.BooleanField(default=True)
    pub_date = models.DateField("Publication date", default=date.today)
    mod_date = models.DateField("Modification date", auto_now=True)
    visits = models.IntegerField(default=0, editable=False)
    objects = StoryManager()

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"
        db_table = "blog_stories"
        ordering = ("-pub_date",)
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
        kwargs = {"year": self.pub_date.year,
                  "month": self.pub_date.strftime("%b").lower(),
                  "day": self.pub_date.day,
                  "slug": self.slug}

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
    # ctype = ContentType.objects.get_for_model(instance)
    # tags = get_tag_list(instance.tags)
    # TaggedItem._default_manager.filter(content_type__pk=ctype.pk,
    #                                    object_id=instance.pk,
    #                                    tag__in=tags).delete()
    # for tag in tags:
    #     if not tag.items.count():
    #         tag.delete()
    for tag in instance.tags.all():
        tag.remove()

post_delete.connect(delete_story_tags, sender=Story)
