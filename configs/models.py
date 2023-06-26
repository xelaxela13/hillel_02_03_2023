from django.db import models

from project.mixins.models import SingletonModel


class Config(SingletonModel, models.Model):
    contact_email = models.EmailField(blank=True, null=True)
