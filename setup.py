import sys
from setuptools import setup, find_packages

from setuptools.command.test import test

def run_tests(*args):
    from blognajd.tests import run_tests, delete_tmp_dirs
    errors = run_tests()
    delete_tmp_dirs()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

test.run_tests = run_tests

setup(
    name = "blognajd",
    version = "1.0",
    packages = find_packages(),
    keywords = "django apps",
    license = "GNU General Public License v3 (GPLv3)",
    description = "Simple django blogging application",
    long_description = "Simple django blogging application. Use it with your customized Twitter-bootstrap theme. Fully tested under django 1.5.1 and python 3.2.",
    author = "Daniel Rus Morales",
    author_email = "inbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "inbox@danir.us",
    url = "http://pypi.python.org/pypi/blognajd/",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    include_package_data = True,
    test_suite = "dummy",
)
