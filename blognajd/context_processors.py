#-*- coding: utf-8 -*-

# Blognajd,
# Copyright (C) 2013, Daniel Rus Morales

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.sites.models import Site
from blognajd.conf import settings as _settings

def settings(request):
    """
    Adds configuration information to the context.

    To employ, add the conf method reference to your project
    settings TEMPLATE_CONTEXT_PROCESSORS.

    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "blognajd.context_processors.settings",
        )
    """
    return {
        'settings': _settings,
        'baseurl': '{0}://{1}'.format(
            request.META.get('wsgi.url_scheme', 'http'),
            Site.objects.get_current().domain)
    }
