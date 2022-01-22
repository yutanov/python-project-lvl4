from django.shortcuts import redirect
from .models import Labels
from .forms import LabelForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from task_manager.mixins import ErrorMessageMixin


class LabelView(ErrorMessageMixin, ListView):
    model = Labels
    template_name = "labels/main.html"
    context_object_name = 'labels'
    login_url = 'login'


class CreateLabel(ErrorMessageMixin, SuccessMessageMixin,
                  CreateView):
    model = Labels
    fields = ['name']
    # form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = '/labels/'
    login_url = 'login'
    success_message = _('SuccessCreatingLabel')


class UpdateLabel(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    template_name = 'labels/update.html'
    form_class = LabelForm
    login_url = 'login'
    success_message = _('SuccessChangingLabel')


class DeleteLabel(ErrorMessageMixin, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete.html'
    success_url = '/labels/'
    context_object_name = 'labels'
    login_url = 'login'
    success_message = _('SuccessDeletingLabel')
    error_url = '/statuses/'

    def delete(self, request, *args, **kwargs):
        if self.get_object().tasks_set.exists():
            messages.error(request, _('CannotDeleteLabel'))
            return redirect(reverse('labels'))
        messages.success(self.request, self.success_message)
        return super(DeleteLabel, self).delete(request, *args, **kwargs)
