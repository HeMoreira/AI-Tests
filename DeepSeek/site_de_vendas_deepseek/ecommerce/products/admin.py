from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'price', 'quantity', 'priority', 'date_added')
    list_filter = ('priority', 'categories', 'date_added')
    search_fields = ('name', 'unique_id', 'description')
    filter_horizontal = ('categories',)
    inlines = [ProductImageInline]
    readonly_fields = ('date_added',)
    fieldsets = (
        (None, {
            'fields': ('unique_id', 'name', 'description', 'short_description')
        }),
        ('Inventory', {
            'fields': ('quantity', 'price', 'priority')
        }),
        ('Media', {
            'fields': ('image', 'categories')
        }),
        ('Metadata', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)