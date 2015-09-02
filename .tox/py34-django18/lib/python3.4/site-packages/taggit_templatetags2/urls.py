from django.conf.urls import patterns, url
from taggit_templatetags2.views import TagCanvasListView


urlpatterns = patterns(
    '',
    url(r'^tag-list/(?P<tag_id>.*)/(?P<tag_slug>.*)/',
        TagCanvasListView.as_view(), name='tagcanvas-list'),
)
