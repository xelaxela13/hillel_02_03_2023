from django.contrib import admin
from django.contrib.auth import get_permission_codename

from products.models import Product, Category
from project.mixins.admins import ImageSnapshotAdminMixin


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'categories_list',
                    'created_at')
    filter_horizontal = ('categories', 'products')
    actions = ['make_is_active']

    def categories_list(self, obj):
        return ','.join(c.name for c in obj.categories.all())

    @admin.action(description="Mark selected products as inactive",
                  permissions=["active"])
    def make_is_active(self, request, queryset):
        queryset.update(is_active=False)

    def has_active_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("active", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    ...
