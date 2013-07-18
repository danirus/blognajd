import sys
from setuptools import setup, find_packages

from setuptools.command.test import test

def run_tests(*args):
    from blognajd.tests import run_tests
    errors = run_tests()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

test.run_tests = run_tests

setup(
    name = "blognajd",
    version = "0.1a",
    packages = find_packages(),
    keywords = "django apps",
    license = "MIT",
    description = "Django blogging app for Python 3, Oh!",
    long_description = "Is it really the first django blogging app for Python 3? Who cares... It is just a simple django blogging app. It uses a customizable/downloadable theme from Twitter-bootstrap. It is fully tested under django 1.5.1 and python 3.2.",
    author = "Daniel Rus Morales",
    author_email = "inbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "inbox@danir.us",
    url = "http://pypi.python.org/pypi/blognajd/",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    include_package_data = True,
    test_suite = "dummy",
)
