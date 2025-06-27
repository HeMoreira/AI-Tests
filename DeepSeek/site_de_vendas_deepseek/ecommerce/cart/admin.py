from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at', 'item_count', 'total_price')
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.item_count()
    item_count.short_description = 'Items'
    
    def total_price(self, obj):
        return f"${obj.total_price()}"
    total_price.short_description = 'Total'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'total_price')
    
    def total_price(self, obj):
        return f"${obj.total_price()}"
    total_price.short_description = 'Total'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)