from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import ugettext as _


class RegisterForm(UserCreationForm):
    name_len = 100
    first_name = forms.CharField(max_length=name_len, label=_('Name'))
    last_name = forms.CharField(max_length=name_len, label=_('LastName'))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2',)
