# blognajd

[![Build Status](https://travis-ci.org/danirus/blognajd.png)](https://travis-ci.org/danirus/blognajd)

Probably the first django blogging app for Python 3. And a twitter-bootstrap customizable theme.

By Daniel Rus Morales <http://danir.us/>

* http://pypi.python.org/pypi/blognajd/
* http://github.com/danirus/blognajd/

Tested under:

* [Python 3.2 and django 1.5.1](http://buildbot.danir.us/builders/blognajd-py32dj15)


## Install the app and the demo site

Steps to install the app and run the demo site:

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


## Tests

Includes a **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with:  ``python setup.py test``


## Theme

The theme is based on Twitter-bootstrap 2.3.2. Customize all the components (colors, fonts, layouts, buttons, navbars, forms, etc) in the [Twitter-bootstrap website](http://twitter.github.io/bootstrap/customize.html). Download the bundle and replace the old `bootstrap.min.css` and `bootstrap.min.js` with your own version in your static directory for blognajd: `static/blognajd/css/` and `static/blognajd/js/`.


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
