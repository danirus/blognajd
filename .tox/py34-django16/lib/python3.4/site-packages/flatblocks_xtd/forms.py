from django.forms import ModelForm

from flatblocks_xtd.models import FlatBlockXtd


class FlatBlockXtdForm(ModelForm):
    class Meta:
        model = FlatBlockXtd
        exclude = ('slug', )
