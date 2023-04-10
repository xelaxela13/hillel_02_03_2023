from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


class FeedbackView(FormView):
    form_class = FeedbackModelForm
    template_name = 'feedbacks/create.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class FeedbackList(ListView):
    template_name = 'feedbacks/index.html'
    model = Feedback
