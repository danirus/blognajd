# blognajd

[![Build Status](https://travis-ci.org/danirus/blognajd.png)](https://travis-ci.org/danirus/blognajd) [![PyPI](https://badge.fury.io/py/blognajd.png)](https://badge.fury.io/py/blognajd)

Simple blogging application, for Python 3.4 and Django 1.7/1.8, with MIT license.

* http://pypi.python.org/pypi/blognajd/
* http://github.com/danirus/blognajd/


## Install the app and the demo site

See the theme section below to download a theme from Twitter-bootstrap, or get the files from this separate repository: [my-blognajd-theme](https://github.com/danirus/my-blognajd-theme). Then follow the next steps to install the application and run the demo site:

    $ pyvenv-3.4 ~/venv/test-blognadj
    $ source venv/test-blognadj/bin/activate
    $ cd ~/venv/test-blognadj
    $ git clone git://github.com/danirus/blognajd.git
    $ cd blognajd
    $ pip install -r requirements_tests.pip
    $ cd example/demo/
    $ python manage.py migrate
    $ python manage.py loaddata initdata.json
    $ python manage.py runserver

Admin access with user **admin**, password **admin**.


## Theme

The 'default' theme is based on Twitter-bootstrap3.

## Settings

There is 1 customizable setting in the settings.py module:

    BLOGNAJD_THEMES_APP_STATIC_PATH = '/path/to/the/static/dir/with/blognajd/themes'

And there are 9 more settings customizable dynamically through the admin interface:
    site_short_name: 'title of the blog'
    site_long_name: 'long description of the site'
    meta_author: 'HTTP meta author'
    meta_keywords: 'HTTP meta keywords'
    meta_description: 'HTTP meta description'
    paginate_by: 10  # the number of stories per page
    truncate_to: 200  # the number of words per story to show in the home
    has_about_page: True  # whether about page is active
    has_projects_page: True  # whether projects page is active
    has_contact_page: True  # whether contact page and form are active

Static pages (about, projects, contact) do exist already. Edit their templates (`blognajd/about.html`, `blognajd/about.html` and `django_contactme/base.html`) and change their texts in the flatblocks_xtd in the admin interface. Better to see it in the demo site.


## Tests

Includes a **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with ``tox``, or, when inside yout own virtualenv, with ``python runtests.py``
