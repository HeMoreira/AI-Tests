from django.contrib import admin
from .models import Categoria, Produto, PerfilCliente, ItemCarrinho

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria_pai', 'descricao']
    list_filter = ['categoria_pai']
    search_fields = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'preco', 'quantidade', 'prioridade', 'ativo', 'data_cadastro']
    list_filter = ['ativo', 'prioridade', 'categorias', 'data_cadastro']
    search_fields = ['codigo', 'nome', 'descricao']
    filter_horizontal = ['categorias']
    readonly_fields = ['data_cadastro']

@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefone', 'genero', 'data_cadastro']
    list_filter = ['genero', 'data_cadastro']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'quantidade', 'data_adicao']
    list_filter = ['data_adicao']
    search_fields = ['user__username', 'produto__nome']