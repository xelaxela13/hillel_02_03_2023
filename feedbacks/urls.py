from django.urls import path

from feedbacks.views import FeedbackView

urlpatterns = [
    path('', FeedbackView.as_view(), name='feedbacks'),
]
