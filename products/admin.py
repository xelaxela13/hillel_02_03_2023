from django.contrib import admin

from products.models import Product, Category
from project.mixins.admins import ImageSnapshotAdminMixin


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'categories_list',
                    'created_at')
    filter_horizontal = ('categories', 'products')

    def categories_list(self, obj):
        return ','.join(c.name for c in obj.categories.all())


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    ...
