from django.contrib import admin
from flatblocks_xtd.models import FlatBlockXtd
from inline_media.admin import AdminTextFieldWithInlinesMixin


class FlatBlockXtdAdmin(AdminTextFieldWithInlinesMixin, admin.ModelAdmin):
    ordering = ['slug', ]
    list_display = ('slug', 'header')
    search_fields = ('slug', 'header', 'content')

admin.site.register(FlatBlockXtd, FlatBlockXtdAdmin)
