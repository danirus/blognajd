============
Instructions
============

This is a reusable django app which adds some templatetags to django-taggit_.

This is a fork the application "django-taggit-templatetags".

django-taggit-templatetags2 requires Django 1.5 or greater.

The application works well under python 3.x

Installation
============

Just install ``django-taggit-templatetags2`` via ``pip``::

    $ pip install django-taggit-templatetags2

After installing and configuring django-taggit_, just add ``taggit_templatetags2`` to your ``INSTALLED_APPS`` in your ``settings.py``::

    INSTALLED_APPS = (
    ...
    'taggit_templatetags2',
    ...
    )

Usage
=====

Now there are some templatetags enabled, at the moment only to create lists of
tags and tag-clouds.

In your templates, you need to load ``taggit_templatetags2_tags``::

    ...
    {% load taggit_templatetags2_tags %}
    ...

---------
Tagdetail
---------

List of tags for the selected object::

   {% get_tags_for_object <some_model_object or id> as "tags" %}

--------
Taglists
--------

After loading ``taggit_templatetags2_tags`` you can create a list of tags for the
whole project (in the sense of djangoproject), for an app (in the sense of djangoapp),
for a model-class (to get a list for an instance of a model, just use its tag-field).

For the tags of a project, just do::

    {% get_taglist as tags %}

For the tags of an app, just do::

    {% get_taglist as tags for 'yourapp' %}

For the tags of a model, just do::

    {% get_taglist as tags for 'yourapp.yourmodel' %}

You can also customize the name of the tags manager in your model (the default is *tags*)::

    {% get_taglist as tags for 'yourapp.yourmodel:yourtags' %}

No matter what you do, you have a list of tags in the ``tags`` template variable.
You can now iterate over it::

    <ul>
    {% for tag in tags %}
    <li>{{tag}} ({{tag.num_times}})</li>
    {% endfor %}
    </ul>

As you can see, each tag has an attribute ``num_times`` which declares how many
times it was used. The list of tags is sorted descending by ``num_times``.

Inclusion-Tag
-------------

For convenience, there's an inclusion-tag. It's used analogue. For example,
for a taglist of a model, just do::

    {% include_taglist 'yourapp.yourmodel' %}

---------
Tagclouds
---------

A very popular way to navigate through tags is a tagcloud_.  This app provides
some tags for that::

    {% get_tagcloud as tags %}

or::

    {% get_tagcloud as tags for 'yourapp' %}

or::

    {% get_tagcloud as tags for 'yourapp.yourmodel' %}

respectivly. The resulting list of tags is ordered by their ``name`` attribute.
Besides the ``num_items`` attribute, there's a ``weight`` attribute. Its maximum
and minimum may be specified as the settings_ section reads.

Inclusion-Tag: tag cloud
------------------------

Even for the tagcloud there's an inclusion-tag. For example, for a tagcloud
of a model, just do::

   {% include_tagcloud 'yourapp.yourmodel' %}


Inclusion-Tag: tag canvas
-------------------------

TagCanvas_ is a Javascript class which will draw and animate a HTML5  canvas
based tag cloud.  You can use this library in your application as follows::

   <!-- Somewhere before the tag include_tagcanvas. For example, in the "head". -->
   {% include "taggit_templatetags2/tagcanvas_include_js_static.html" %}

   {% include_tagcanvas 'element_id' 'width px' 'height px' 'some-url-name' 'yourapp.yourmodel' %}

- element_id - name to create identifiers for html tags
- some-url-name -  url to view a list of objects for the selected tag. Default: *tagcanvas-list*.
   For example, some-url-name='myurlname', then it must be an entry in urls.py
   file like this::

   from taggit_templatetags2.views import TagCanvasListView

   urlpatterns = patterns(
       ...
       url(r'^tag-list/(?P<tag_id>.*)/(?P<tag_slug>.*)/',
           TagCanvasListView.as_view(), name='myurlname'),
   )

Or you can use the default view, and then you have to add the following things:

- in urls.py::

   from taggit_templatetags2 import urls as taggit_templatetags2_urls
   urlpatterns = patterns(
       ...
       url(r'^tags/', include('taggit_templatetags2.urls')),
   )

- override template "taggit_templatetags2/tagcanvas_base.html" and
- override template "taggit_templatetags2/tagcanvas_list_item.html" to customize the look

To use this inclusion-tag, make sure that 'django.core.context_processors.static'
appears somewhere in your TEMPLATE_CONTEXT_PROCESSORS setting.



.. _settings:

Settings
========

There are a few settings to be set:

TAGGIT_TAGCLOUD_MIN (default: 1.0)
    This specifies the minimum of the weight attribute of a tagcloud's tags.

TAGGIT_TAGCLOUD_MAX (default: 6.0)
    This specifies the maximum of the weight attribute of a tagcloud's tags.

If you want to use the weight as font-sizes, just do as follows::

    <font size={{tag.weight|floatformat:0}}>{{tag}}</font>

So the weights are converted to integer values.

If you're using your own Tag and/or TaggedItem models rather than the default
ones (`Custom Tagging`_), you can specify a tuple for each model (app,model_name)

TAGGIT_TAG_MODEL = ('myapp','MyTag')
   default: ('taggit', 'Tag')

TAGGIT_TAGGED_ITEM_MODEL = ('myapp','MyTaggedItem')
   default: ('taggit', 'TaggedItem')

TAGGIT_LIMIT = 234
   Number items for tag cloud.
   default: 10

TAGGIT_TAG_LIST_ORDER_BY = 'name'
   Order for the queryset used to generate the list.
   default: -num_times

TAGGIT_TAG_CLOUD_ORDER_BY = '-num_times'
   Order for the queryset used to generate the list.
   default: name

Testing
=======

Clone code repository::

   $ git clone https://github.com/fizista/django-taggit-templatetags.git

Installation dependencies needed to test the application::

   $ pip install -e <path to the application>[tests]

Starting tests::

   $ python ./develop.py test

Starting test coverage::

   $ python ./develop.py manage test

Starting tox tests::

   $ tox

Thanks
======

Thanks to the python- and django-community, in particular to `Alex Gaynor`_,
the inventor of django-taggit_ and a wonderful guy to argue with.
Thanks to `Mathijs de Bruin`_ as well for his helpful pull requests.

.. _django-taggit: http://pypi.python.org/pypi/django-taggit
.. _tagcloud: http://www.wikipedia.org/wiki/Tagcloud
.. _Alex Gaynor: http://alexgaynor.net/
.. _Mathijs de Bruin: http://github.com/dokterbob
.. _Custom Tagging: http://django-taggit.readthedocs.org/en/latest/custom_tagging.html
.. _TagCanvas: http://www.goat1000.com/tagcanvas.php


