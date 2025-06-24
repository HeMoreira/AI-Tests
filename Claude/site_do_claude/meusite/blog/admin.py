from django.contrib import admin
from .models import Categoria, Post, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome']
    list_filter = ['criado_em']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'status', 'criado_em', 'visualizacoes']
    list_filter = ['status', 'categoria', 'criado_em', 'autor']
    search_fields = ['titulo', 'conteudo']
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ['autor']
    date_hierarchy = 'criado_em'
    ordering = ['-criado_em']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'post', 'criado_em', 'ativo']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'email', 'conteudo']
    actions = ['aprovar_comentarios']
    
    def aprovar_comentarios(self, request, queryset):
        queryset.update(ativo=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"