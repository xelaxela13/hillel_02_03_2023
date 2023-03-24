# from os import path
import uuid

from django.db import models


# def upload_to(instance, filename):
#     _name, extension = path.splitext(filename)
#     return f'products/images/{str(instance.pk)}{extension}'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    # image = models.ImageField(upload_to=upload_to)
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
