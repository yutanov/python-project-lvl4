from django.shortcuts import redirect
from .models import Tasks
from .forms import TasksForm
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .filters import TasksFilter
from django.contrib import messages
from django.utils.translation import ugettext as _
from django_filters.views import FilterView
from task_manager.mixins import ErrorMessageMixin


class TasksList(ErrorMessageMixin, FilterView):
    model = Tasks
    template_name = "tasks/main.html"
    context_object_name = 'tasks'
    login_url = 'login'
    filterset_class = TasksFilter


class ShowTask(ErrorMessageMixin, DetailView):
    model = Tasks
    template_name = 'tasks/detail.html'
    login_url = 'login'


class CreateTask(ErrorMessageMixin, SuccessMessageMixin, CreateView):
    """Task create view."""

    model = Tasks
    fields = ['name', 'description', 'status', 'executor', 'label']
    template_name = 'tasks/create.html'
    success_url = '/tasks/'
    login_url = 'login'
    success_message = _('SuccessCreatingTask')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateTask(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/update.html'
    form_class = TasksForm
    login_url = 'login'
    success_message = _('SuccessChangingTask')


class DeleteTask(ErrorMessageMixin, UserPassesTestMixin,
                 SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = '/tasks/'
    login_url = 'tasks'
    success_message = _('SuccessDeletingTask')

    def test_func(self):
        obj = self.get_object()
        user_is_creator = obj.creator == self.request.user
        if not user_is_creator:
            messages.error(self.request, _('CannotDeleteTask'))
        return user_is_creator

    def handle_no_permission(self):
        return redirect(self.login_url)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTask, self).delete(request, *args, **kwargs)
