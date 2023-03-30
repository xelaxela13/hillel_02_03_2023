from django.urls import path

from feedbacks.views import feedbacks

urlpatterns = [
    path('', feedbacks, name='feedbacks'),
]
