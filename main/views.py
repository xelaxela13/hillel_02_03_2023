from django.core.mail import mail_admins
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView

from main.forms import ContactForm


class MainView(TemplateView):
    template_name = 'main/index.html'


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contacts/index.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        msg = f'FROM: ' \
              f'{form.cleaned_data["email"]}\n{form.cleaned_data["text"]}'
        # todo move to celery task
        mail_admins(_('Contact form'), msg)
        return super().form_valid(form)
