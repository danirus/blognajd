#-*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from inline_media.admin import AdminTextFieldWithInlinesMixin
from inline_media.widgets import TextareaWithInlines

from blognajd.models import Story


class StoryAdmin(AdminTextFieldWithInlinesMixin, admin.ModelAdmin):
    list_display  = ("title", "pub_date", "mod_date", "status", "visits")
    list_filter   = ("status", "pub_date")
    search_fields = ("title", "abstract", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug", "markup",
                                    "abstract", "body",)}),
                 ("Post data", {"fields": ("status", 
                                           ("allow_comments", "tags"),
                                           ("pub_date",)),}),
                 ("Converted markup", {"classes": ("collapse",),
                                       "fields": ("abstract_markup", 
                                                  "body_markup",),}),)
      
admin.site.register(Story, StoryAdmin)
