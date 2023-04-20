from django.db.models.signals import m2m_changed

from products.models import Product


def product_categories_change(sender, action, **kwargs):
    ...


m2m_changed.connect(product_categories_change,
                    sender=Product.categories.through)
