from django.contrib import admin
from .models import Categoria, Produto, Cliente, Carrinho, ItemCarrinho

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)