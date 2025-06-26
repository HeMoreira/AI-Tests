from django.shortcuts import render
from produtos.models import Produto
from produtos.models import Produto, Categoria
from django.db.models import Q

def home(request):
    destaques = Produto.objects.order_by('-prioridade')[:6]
    novidades = Produto.objects.order_by('-data_cadastro')[:6]
    return render(request, 'loja/home.html', {
        'destaques': destaques,
        'novidades': novidades
    })

def lista_produtos(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.filter(categoria_pai__isnull=True)

    # Filtros
    nome = request.GET.get('nome')
    categoria_id = request.GET.get('categoria')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if nome:
        produtos = produtos.filter(nome__icontains=nome)

    if categoria_id:
        produtos = produtos.filter(categorias__id=categoria_id)

    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)

    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    produtos = produtos.order_by('-prioridade', '-data_cadastro')

    return render(request, 'loja/lista_produtos.html', {
        'produtos': produtos,
        'categorias': categorias
    })