# blognajd

[![Build Status](https://travis-ci.org/danirus/blognajd.png)](https://travis-ci.org/danirus/blognajd) [![Downloads](https://pypip.in/d/blognajd/badge.png)](https://pypi.python.org/pypi/blognajd)

Simple django blogging application, for Python 3, licensed under the GNU GPLv3.

* http://pypi.python.org/pypi/blognajd/
* http://github.com/danirus/blognajd/

Tested under:

* [Python 3.2 and django 1.5.1](http://buildbot.danir.us/builders/blognajd-py32dj15)


## Install the app and the demo site

See the theme section below to download a theme from Twitter-bootstrap, or get the files from this separate repository: [my-blognajd-theme](https://github.com/danirus/my-blognajd-theme). Then follow the next steps to install the application and run the demo site:

    $ virtualenv -p python3 ~/venv/test-blognadj
    $ source venv/test-blognadj/bin/activate
    $ cd ~/venv/test-blognadj
    $ git clone git://github.com/danirus/blognajd.git
    $ cd blognajd
    $ pip install -r requirements_tests.pip
    $ cd example/demo/
    $ python manage.py syncdb --noinput
    $ python manage.py runserver

Admin access with user **admin**, password **admin**.


## Theme

The theme is based on Twitter-bootstrap 2.3.2 and its files are not provided within blognajd due to license incompatilibity. 

Go to the [Twitter-bootstrap website](http://twitter.github.io/bootstrap/customize.html) and customize all the components (colors, fonts, layouts, buttons, navbars, forms, etc). Download the bundle and copy `css/bootstrap.min.css` and `js/bootstrap.min.js` to your blognajd static directory `static/blognajd.


## Settings

There are 10 customizable settings:

    BLOGNAJD_SITE_SHORT_NAME = 'sitename'
    BLOGNAJD_SITE_LONG_NAME = 'for the html title and such'
    BLOGNAJD_META_AUTHOR = 'Joe Bloggs'
    BLOGNAJD_META_KEYWORDS = 'this that theotherthing'
    BLOGNAJD_META_DESCRIPTION = 'Once upon a time...'
    BLOGNAJD_PAGINATE_BY = 10 # number of stories per page
    BLOGNAJD_TRUNCATE_TO = 200 # number of words per story to show in the home
    BLOGNAJD_HAS_ABOUT = True # whether about page is active
    BLOGNAJD_HAS_PROJECTS = True # whether projects page is active
    BLOGNAJD_HAS_CONTACT = True # whether contact page and form are active

Static pages (about, projects, contact) do exist already. Edit their templates (`blognajd/about.html`, `blognajd/about.html` and `django_contactme/base.html`) and change their texts in the flatblocks_xtd in the admin interface. Better to see it in the demo site.


## Tests

Includes a **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with:  ``python setup.py test``
