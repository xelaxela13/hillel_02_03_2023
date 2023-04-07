from django.views.generic import FormView

from feedbacks.model_forms import FeedbackModelForm


class FeedbackView(FormView):
    form_class = FeedbackModelForm
    template_name = 'feedbacks/index.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
