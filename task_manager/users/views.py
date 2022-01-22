from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import UpdateView, DeleteView, ListView
from django.urls import reverse
from .models import CustomUser
from django.db import models
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import View
from django.core.exceptions import ImproperlyConfigured


class ErrorMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('NotLoginStatus'))
            return self.handle_no_permission()
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(request, _('UserNoPermission'))
            return redirect(reverse('users'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        return redirect(self.login_url)


class UserList(ListView):
    model = CustomUser
    template_name = "users/main.html"
    context_object_name = 'users'


class UserUpdateView(ErrorMessageMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users/update.html'
    form_class = RegisterForm
    success_url = '/users/'
    login_url = 'login'
    success_message = _('SuccessUpdateUser')


class UserDeleteView(ErrorMessageMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = '/users/'
    login_url = 'login'
    error_url = '/users/'

    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured("No error URL to redirect to.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        error_url = self.get_error_url()
        try:
            self.object.delete()
            messages.success(request, _('SuccessDeletingUser'))
            return HttpResponseRedirect(success_url)
        except models.ProtectedError:
            messages.error(request, _('CannotDeleteUser'))
            return HttpResponseRedirect(error_url)


class RegisterView(FormView):
    form_class = RegisterForm
    success_url = "/login/"
    template_name = "users/create.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        messages.success(self.request, _('SuccessRegistrationUser'))

        # Вызываем метод базового класса
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "users/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        messages.success(self.request, _('YouIn'))
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)
        messages.info(self.request, _('YouOut'))

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")
