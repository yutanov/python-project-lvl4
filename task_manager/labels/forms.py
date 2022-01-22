from .models import Labels
from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext as _


class LabelForm(ModelForm):
    class Meta:
        model = Labels
        fields = ['name']

        widgets = {'name': TextInput(attrs={'class': 'form-control',
                                            'placeholder': _('Name')	})}
