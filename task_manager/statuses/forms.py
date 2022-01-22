from .models import Statuses
from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext as _


class StatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ['name']

        widgets = {'name': TextInput(attrs={'class': 'form-control',
                                            'placeholder': _('Name')})}
