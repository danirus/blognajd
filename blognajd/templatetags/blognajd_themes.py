# ----------------------------------------------------------------------
# This file is basically a copy of
# django/contrib/staticfiles/templatetags/staticfiles.py
#
# It provides the templatetag theme_static, which returns the URL to a file
# using the staticfiles' storage backend, appended to the theme chosen by
# the admin user in the dynamic settings.

import os.path

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import StaticNode

from usersettings.shortcuts import get_current_usersettings
from blognajd.conf import settings


register = template.Library()
themes_path = getattr(settings, 'BLOGNAJD_THEMES_APP_STATIC_PATH', '')


def theme_static(path):
    return staticfiles_storage.url(path)


class StaticFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        dynconf = get_current_usersettings()
        return theme_static(os.path.join(themes_path, dynconf.theme, path))


@register.tag('theme_static')
def do_theme_static(parser, token):
    """
    A template tag that returns the URL to a theme file
    using staticfiles' storage backend.

    Usage::

        {% theme_static [as varname] %}

    Examples::

        {% theme_static 'myapp/css/base.css' %}
        {% theme_static variable_with_path %}
        {% theme_static "myapp/css/base.css" as admin_base_css %}
        {% theme_static variable_with_path as varname %}

    """
    return StaticFilesNode.handle_token(parser, token)
