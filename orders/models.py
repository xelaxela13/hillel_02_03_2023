import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from django_lifecycle import LifecycleModelMixin, AFTER_SAVE, hook, \
    AFTER_UPDATE

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes

User = get_user_model()


class Discount(PKMixin):
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    code = models.CharField(
        max_length=32,
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"

    @property
    def is_valid(self):
        is_valid = self.is_active
        if self.valid_until:
            is_valid &= timezone.now() <= self.valid_until
        return is_valid


class Order(LifecycleModelMixin, PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        User,
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
    order_number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    def __str__(self):
        return f"{self.user} | {self.total_amount}"

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        total_amount = self.order_items.aggregate(
            total_amount=Sum(F('price') * F('quantity'))
        )['total_amount'] or 0
        total_amount = decimal.Decimal(total_amount)
        if self.discount and self.discount.is_valid:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (total_amount / 100 * self.discount.amount)
            ).quantize(decimal.Decimal('.01'))
        return total_amount

    @hook(AFTER_UPDATE, when='discount', has_changed=True)
    def set_total_amount(self):
        self.total_amount = self.get_total_amount()
        self.save(update_fields=('total_amount',), skip_hooks=True)


class OrderItem(LifecycleModelMixin, PKMixin):
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

    @property
    def sub_total(self):
        return self.price * self.quantity

    @hook(AFTER_SAVE)
    def set_order_total_amount(self):
        self.order.total_amount = self.order.get_total_amount()
        self.order.save(update_fields=('total_amount',), skip_hooks=True)
