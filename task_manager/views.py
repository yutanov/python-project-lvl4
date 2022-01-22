from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    context = {
        'hello': _('Hello')
    }
    return render(request, 'task_manager/index.html', context)
