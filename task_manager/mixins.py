from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin


class ErrorMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('NotLoginStatus'))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
