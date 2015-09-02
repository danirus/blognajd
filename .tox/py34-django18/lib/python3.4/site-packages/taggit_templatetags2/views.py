from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from .settings import TAGGED_ITEM_MODEL, TAG_MODEL


class TagCanvasListView(ListView):

    template_name = 'taggit_templatetags2/tagcanvas_list.html'

    model = TAGGED_ITEM_MODEL

    def get_tag_id(self):
        return int(self.kwargs['tag_id'])

    def get_tag_object(self):
        return TAG_MODEL.objects.get(id=self.get_tag_id())

    def get_queryset(self):
        """
        Returns only the objects assigned to single tag.

        """
        return self.model._default_manager.filter(
            tag_id=self.get_tag_id())

    def get_context_data(self, **kwargs):
        context = super(TagCanvasListView, self).get_context_data(**kwargs)
        context['tag'] = self.get_tag_object()
        return context
