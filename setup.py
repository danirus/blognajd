import sys
from setuptools import setup, find_packages
from setuptools.command.test import test

def TestCommand(test):
    def run(self):
        import pytest
        from blognajd.tests import setup_django_settings
        setup_django_settings()
        pytest.main(['-v',])

# def run_tests(*args):
#     from blognajd.tests import run_tests, delete_tmp_dirs
#     errors = run_tests()
#     delete_tmp_dirs()
#     if errors:
#         sys.exit(1)
#     else:
#         sys.exit(0)

# test.run_tests = run_tests

setup(
    name = "blognajd",
    version = "1.1",
    packages = find_packages(),
    keywords = "django apps",
    license = "MIT",
    description = "Simple django blogging application",
    long_description = "A simple pluggable well maintained django blogging application, tested and fully compatible with Django 1.8 and Python 3.4.",
    author = "Daniel Rus Morales",
    author_email = "mbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "mbox@danir.us",
    url = "http://pypi.python.org/pypi/blognajd/",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Framework :: Django',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
    ],
    include_package_data = True,
    cmdclass={'test': TestCommand},
)
