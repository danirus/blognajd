from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inline_media.admin import AdminTextFieldWithInlinesMixin
from usersettings.admin import SettingsAdmin

from blognajd.models import SiteSettings, Story


class SiteSettingsAdmin(SettingsAdmin):
    list_display = ('site_short_name',)
    fieldsets = ((None, {'fields': (('site_short_name', 'site_long_name'),
                                    'theme')}),
                 (_('Meta tags'), {
                     'fields': ('meta_author', 'meta_keywords',
                                'meta_description')}),
                 (_('Extra settings'), {
                     'fields': ('paginate_by', 'truncate_to')}),
                 (_('Enable additional pages'), {
                     'fields': ('has_about_page', 'has_projects_page',
                                'has_contact_page')}))

admin.site.register(SiteSettings, SiteSettingsAdmin)


class StoryAdmin(AdminTextFieldWithInlinesMixin, admin.ModelAdmin):
    list_display = ("title", "pub_date", "mod_date", "status", "visits")
    list_filter = ("status", "pub_date")
    search_fields = ("title", "abstract", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug", "markup",
                                    "abstract", "body",)}),
                 ("Post data", {"fields": ("status",
                                           ("allow_comments", "tags"),
                                           ("pub_date",)), }),
                 ("Converted markup", {"classes": ("collapse",),
                                       "fields": ("abstract_markup",
                                                  "body_markup",), }),)

admin.site.register(Story, StoryAdmin)
