# orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price_at_purchase', 'total_item_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'customer')
    search_fields = ('order_number', 'customer__username', 'shipping_address')
    readonly_fields = ('order_number', 'total_amount', 'created_at', 'updated_at', 'shipping_address')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('customer', 'order_number', 'total_amount', 'created_at', 'updated_at')
        }),
        ('Informações de Status', {
            'fields': ('status', 'payment_method', 'payment_status')
        }),
        ('Endereço de Entrega', {
            'fields': ('shipping_address',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price_at_purchase', 'total_item_price')
    list_filter = ('order', 'product')
    search_fields = ('product_name', 'order__order_number')
    readonly_fields = ('total_item_price',)