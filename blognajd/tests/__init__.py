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

import os
import shutil
import six
import sys
import unittest

def setup_django_settings():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def run_tests():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()

    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_suite = TestRunner(verbosity=2, interactive=True, failfast=False)
    test_suite.run_tests(["blognajd"])


def delete_tmp_dirs():
    from django.conf import settings
    try:
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'pictures'))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'cache'))
    except OSError as exc:
        if exc.errno != 2:
            six.reraise(e)

def suite():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()
    else:
        from django.db.models.loading import load_app
        from django.conf import settings
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ['blognajd.tests',]
        map(load_app, settings.INSTALLED_APPS)
    
    from blognajd.tests import (test_urls, test_views, 
                                test_context_preprocessor, test_feeds,
                                test_models, test_sitemaps)

    testsuite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_urls),
        unittest.TestLoader().loadTestsFromModule(test_views), 
        unittest.TestLoader().loadTestsFromModule(test_context_preprocessor),
        unittest.TestLoader().loadTestsFromModule(test_feeds), 
        unittest.TestLoader().loadTestsFromModule(test_models),
        unittest.TestLoader().loadTestsFromModule(test_sitemaps),
    ])
    return testsuite


if __name__ == "__main__":
    run_tests()
