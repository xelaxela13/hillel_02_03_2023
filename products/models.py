from os import path

from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    AFTER_CREATE

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies, ProductCacheKeys


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Product(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    currency = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )

    def __str__(self):
        return f"{self.name} - {self.price}"

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(ProductCacheKeys.PRODUCTS)
