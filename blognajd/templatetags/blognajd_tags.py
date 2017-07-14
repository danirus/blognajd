from __future__ import unicode_literals

from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from taggit_templatetags2 import settings

register = template.Library()


@register.tag
class GetTagForObject(AsTag):

    name = 'get_tags_for_object'

    options = Options(
        Argument('source_object', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, source_object, varname=''):
        """
        Args:
            source_object - <django model object>

        Return:
            queryset tags
        """

        tag_model = settings.TAG_MODEL
        app_label = source_object._meta.app_label
        model = source_object._meta.model_name
        content_type = ContentType.objects.get(app_label=app_label,
                                               model=model)

        try:
            tags = tag_model.objects.filter(
                taggit_taggeditem_items__object_id=source_object,
                taggit_taggeditem_items__content_type=content_type)
        except:
            tags = tag_model.objects.filter(
                taggit_taggeditem_items__object_id=source_object.id,
                taggit_taggeditem_items__content_type=content_type)

        if varname:
            context[varname]
            return ''
        else:
            return tags
