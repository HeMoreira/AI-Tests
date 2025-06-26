from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria
from django.shortcuts import redirect
from .models import Produto, Cliente, ItemCarrinho, Carrinho
from django.contrib.auth.decorators import login_required
from .models import Pedido
from django.db import transaction


def pagina_inicial(request):
    produtos = Produto.objects.all().order_by('-prioridade')[:10]
    return render(request, 'loja/index.html', {'produtos': produtos})

def lista_produtos(request):
    produtos = Produto.objects.all()
    nome = request.GET.get('nome')
    categoria = request.GET.get('categoria')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if nome:
        produtos = produtos.filter(nome__icontains=nome)
    if categoria:
        produtos = produtos.filter(categorias__nome__icontains=categoria)
    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    categorias = Categoria.objects.all()

    return render(request, 'loja/lista_produtos.html', {
        'produtos': produtos.distinct(),
        'categorias': categorias
    })


def info_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'loja/info_produto.html', {'produto': produto})

def carrinho(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cliente = request.user.cliente
    carrinho = cliente.carrinho
    return render(request, 'loja/carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    cliente = request.user.cliente
    carrinho, _ = Carrinho.objects.get_or_create(cliente=cliente)
    produto = get_object_or_404(Produto, id=produto_id)

    item, criado = ItemCarrinho.objects.get_or_create(produto=produto)
    if item in carrinho.itens.all():
        item.quantidade += 1
        item.save()
    else:
        item.quantidade = 1
        item.save()
        carrinho.itens.add(item)

    return redirect('carrinho')

@login_required
def remover_do_carrinho(request, item_id):
    cliente = request.user.cliente
    carrinho = cliente.carrinho
    item = get_object_or_404(ItemCarrinho, id=item_id)
    carrinho.itens.remove(item)
    item.delete()
    return redirect('carrinho')

@login_required
def atualizar_quantidade(request, item_id):
    if request.method == 'POST':
        nova_qtd = int(request.POST.get('quantidade'))
        item = get_object_or_404(ItemCarrinho, id=item_id)
        item.quantidade = nova_qtd
        item.save()
    return redirect('carrinho')

from .models import Pedido
from django.db import transaction

@login_required
@transaction.atomic
def finalizar_pedido(request):
    cliente = request.user.cliente
    carrinho = cliente.carrinho
    itens = carrinho.itens.all()

    if not itens:
        return redirect('carrinho')  # ou mostrar mensagem "Carrinho vazio"

    total = carrinho.total()

    pedido = Pedido.objects.create(cliente=cliente, total=total)
    for item in itens:
        pedido.itens.add(item)

    carrinho.itens.clear()

    return render(request, 'loja/pedido_confirmado.html', {'pedido': pedido})

@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user.cliente).order_by('-data_pedido')
    return render(request, 'loja/meus_pedidos.html', {'pedidos': pedidos})