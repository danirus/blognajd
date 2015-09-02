from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION[0:2] < (1, 4):
    from django.conf.urls.defaults import patterns, url
else:
    from django.conf.urls import patterns, url

from django.contrib.admin.views.decorators import staff_member_required
from flatblocks_xtd.views import edit

urlpatterns = patterns('',
    url('^edit/(?P<pk>\d+)/$', staff_member_required(edit),
            name='flatblocks-xtd-edit')
)
