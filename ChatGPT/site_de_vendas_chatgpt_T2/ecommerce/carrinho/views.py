from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, ItemCarrinho
from produtos.models import Produto
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente

@login_required
def ver_carrinho(request):
    cliente = request.user.cliente
    carrinho = cliente.carrinho
    return render(request, 'carrinho/ver_carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    cliente = request.user.cliente
    carrinho = cliente.carrinho
    produto = get_object_or_404(Produto, id=produto_id)

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho, produto=produto,
        defaults={'quantidade': 1}
    )

    if not created:
        item.quantidade += 1
        item.save()

    return redirect('ver_carrinho')

@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    item.delete()
    return redirect('ver_carrinho')
