#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F, Q
from django.http import (HttpResponseNotFound, HttpResponseServerError, 
                         HttpResponseForbidden, HttpResponseRedirect, Http404)
from django.shortcuts import render_to_response as render
from django.template import loader, RequestContext
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import View, ListView, DateDetailView, RedirectView
from django.views.generic.dates import (YearArchiveView, MonthArchiveView, 
                                        DayArchiveView)
from django.views.generic.list import MultipleObjectMixin

from tagging.models import Tag, TaggedItem

from blognajd.models import DRAFT, PUBLIC, Story


def http403_handler(request):
    t = loader.get_template("blognajd/403.html")
    return HttpResponseForbidden(
        t.render(RequestContext(request, {'request_path': request.path})))

def http404_handler(request):
    t = loader.get_template("blognajd/404.html")
    return HttpResponseNotFound(
        t.render(RequestContext(request, {'request_path': request.path})))

def http500_handler(request):
    t = loader.get_template("blognajd/500.html")
    return HttpResponseServerError(
        t.render(RequestContext(request, {'request_path': request.path})))

class HomepageView(ListView):
    template_name = "blognajd/index.html"

    def get_paginate_by(self, queryset):
        return settings.BLOGNAJD_PAGINATE_BY

    def get_queryset(self):
        if self.request.session.get("unpublished_on", False):
            status = [DRAFT, PUBLIC]
        else:
            status = [PUBLIC]
        return Story.objects.select(status).order_by('-pub_date')
    

@login_required(redirect_field_name="")
def show_unpublished(request):
    redirect_to = request.REQUEST.get("next", '/')
    request.session["unpublished_on"] = True
    return HttpResponseRedirect(redirect_to)


@login_required(redirect_field_name="")
def hide_unpublished(request):
    redirect_to = request.REQUEST.get("next", '/')
    request.session["unpublished_on"] = False
    return HttpResponseRedirect(redirect_to)


class StoryDetailView(DateDetailView):
    def get_queryset(self):
        return self.model.objects.published()
        
    def get_object(self, *args, **kwargs):
        qs = super(DateDetailView, self).get_object(*args, **kwargs)
        if qs.status == PUBLIC and not qs.in_the_future:
            qs.visits = F('visits') + 1
            qs.save()
        return qs


class BlogViewMixin(MultipleObjectMixin):
    def get_queryset(self):
        if self.request.session.get("unpublished_on", False):
            qs = self.model.objects.filter(status__in=[DRAFT,PUBLIC])
        else:
            qs = self.model.objects.filter(status=PUBLIC, pub_date__lte=now())
        return qs


class StoryListView(ListView, BlogViewMixin):
    pass

class ArchiveView(BlogViewMixin, YearArchiveView):
    date_field = "pub_date"
    make_object_list = True

class ArchiveRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            latest = Story.objects.latest('pub_date')
        except Story.DoesNotExist:
            return '/'
        else:
            return reverse('archive-year', 
                           kwargs={'year':latest.pub_date.year})

class TagDetailView(ListView):
    """
    Paginated tag list

    Template: ``blognajd/tag_detail.html``
    Context:
        object_list
            List of tags.
    """
    model = Tag
    slug_field = "name"
    template_name = "blognajd/tag_detail.html"

    def get_paginate_by(self, queryset):
        return settings.BLOGNAJD_PAGINATE_BY

    def get_queryset(self):
        return TaggedItem.objects.filter(
            tag__name__iexact=self.kwargs.get("slug", "")).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        try:
            context["object"] = Tag.objects.get(
                name=self.kwargs.get("slug", ""))
        except Tag.DoesNotExist:
            raise Http404("Tag '{0}' does not exist".format(
                    self.kwargs.get("slug", "")))
        return context
