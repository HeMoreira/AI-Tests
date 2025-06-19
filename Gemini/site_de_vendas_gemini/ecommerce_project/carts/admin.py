# carts/admin.py

from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline): # TabularInline para lista compacta de itens
    model = CartItem
    extra = 0 # Não mostra campos extras vazios
    readonly_fields = ('price_at_addition',) # Preço na adição não pode ser alterado aqui

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at', 'total_price', 'total_items')
    search_fields = ('customer__username', 'customer__email')
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'total_items')
    inlines = [CartItemInline]

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Valor Total"

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = "Total de Itens"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price_at_addition', 'total_price', 'added_at')
    list_filter = ('cart__customer', 'product')
    search_fields = ('product__name', 'cart__customer__username')
    readonly_fields = ('price_at_addition', 'total_price', 'added_at')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Preço Total do Item"