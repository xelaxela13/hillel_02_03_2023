from django.contrib import admin
from django.contrib.admin import TabularInline

from orders.models import Order, OrderItem, Discount


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ...


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    ...
