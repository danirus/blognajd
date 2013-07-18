from django import VERSION as DJANGO_VERSION
from django.conf.urls import include, patterns, url

from django.conf import settings

from blognajd.urls import handler403, handler404, handler500

urlpatterns = patterns(
    '',
    url(r'',        include('blognajd.urls')),
)
