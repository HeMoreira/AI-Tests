# products/admin.py

from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity', 'priority', 'is_active', 'created_at')
    list_filter = ('is_active', 'categories', 'created_at')
    search_fields = ('name', 'short_description', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',) # Melhora a interface para ManyToMany
    fieldsets = (
        (None, {
            'fields': ('name', 'sku', 'slug', 'short_description', 'description', 'image', 'categories', 'priority')
        }),
        ('Informações de Preço e Estoque', {
            'fields': ('price', 'quantity', 'is_active')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Colapsa a seção por padrão
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'sku') # SKU será gerado, não editado.