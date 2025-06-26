from django.contrib import admin
from .models import Pedido, Produto, Categoria, Cliente, Carrinho, ItemCarrinho

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade', 'prioridade', 'data_cadastro')
    search_fields = ('nome',)
    list_filter = ('categorias', 'data_cadastro')

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'status', 'data_pedido')
    list_filter = ('status', 'data_pedido')
    search_fields = ('cliente__usuario__username',)

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)