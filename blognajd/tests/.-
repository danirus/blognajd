from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from easy_blog.sitemaps import StoriesSitemap

admin.autodiscover()

urlpatterns = patterns('demo.views',
    url(r'^admin/',           include(admin.site.urls)),
    url(r'^blog/',            include('easy_blog.urls')),
    url(r"^comments/",        include("django_comments_xtd.urls")),
    url(r'^$',                'index',              name='index'),
)

sitemaps = {
    'stories': StoriesSitemap,
}

urlpatterns += patterns("django.contrib.sitemaps.views",
    url(r'^sitemap\.xml$',                 'index',   {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        "",
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
        }),
    )
