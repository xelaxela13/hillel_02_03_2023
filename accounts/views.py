from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from accounts.model_forms import RegistrationForm, AuthenticationForm


class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(AuthLoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, _('Welcome back!'))
        return HttpResponseRedirect(self.get_success_url())
