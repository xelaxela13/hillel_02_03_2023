import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes


class Discount(PKMixin):
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self):
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    def __str__(self):
        return f"{self.user} | {self.get_total_amount()}"

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        total_amount = self.order_items.aggregate(
            total_amount=Sum(F('price') * F('quantity'))
        )['total_amount'] or 0
        if self.discount and self.discount.is_active:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (total_amount / 100 * self.discount.amount)
            ).quantize(decimal.Decimal('.01'))
        return total_amount


class OrderItem(PKMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    class Meta:
        unique_together = ('order', 'product')
