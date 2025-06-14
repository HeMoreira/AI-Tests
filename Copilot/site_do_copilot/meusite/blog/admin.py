from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')  # Mostra esses campos na lista
    search_fields = ('titulo',)  # Adiciona busca por título

admin.site.register(Post, PostAdmin)