from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Produto, Categoria, ItemCarrinho, PerfilCliente
from .forms import CustomUserCreationForm, FiltrosProdutoForm

def home(request):
    produtos_destaque = Produto.objects.filter(ativo=True, prioridade__lte=2)[:8]
    produtos_recentes = Produto.objects.filter(ativo=True).order_by('-data_cadastro')[:6]
    categorias_principais = Categoria.objects.filter(categoria_pai=None)[:6]
    
    context = {
        'produtos_destaque': produtos_destaque,
        'produtos_recentes': produtos_recentes,
        'categorias_principais': categorias_principais,
    }
    return render(request, 'loja/home.html', context)

def lista_produtos(request):
    form = FiltrosProdutoForm(request.GET)
    produtos = Produto.objects.filter(ativo=True)
    
    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        categoria = form.cleaned_data.get('categoria')
        preco_min = form.cleaned_data.get('preco_min')
        preco_max = form.cleaned_data.get('preco_max')
        ordenacao = form.cleaned_data.get('ordenacao')
        
        if nome:
            produtos = produtos.filter(Q(nome__icontains=nome) | Q(descricao_curta__icontains=nome))
        
        if categoria:
            produtos = produtos.filter(Q(categorias=categoria) | Q(categorias__categoria_pai=categoria)).distinct()
        
        if preco_min:
            produtos = produtos.filter(preco__gte=preco_min)
        
        if preco_max:
            produtos = produtos.filter(preco__lte=preco_max)
        
        if ordenacao:
            produtos = produtos.order_by(ordenacao)
    
    context = {
        'produtos': produtos,
        'form': form,
        'total_produtos': produtos.count(),
    }
    return render(request, 'loja/lista_produtos.html', context)

def detalhe_produto(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo, ativo=True)
    produtos_relacionados = Produto.objects.filter(
        categorias__in=produto.categorias.all(),
        ativo=True
    ).exclude(id=produto.id).distinct()[:4]
    
    context = {
        'produto': produto,
        'produtos_relacionados': produtos_relacionados,
    }
    return render(request, 'loja/detalhe_produto.html', context)

@login_required
def carrinho(request):
    itens = ItemCarrinho.objects.filter(user=request.user).select_related('produto')
    total = sum(item.get_subtotal() for item in itens)
    total_formatado = f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    context = {
        'itens': itens,
        'total': total,
        'total_formatado': total_formatado,
    }
    return render(request, 'loja/carrinho.html', context)

@login_required
@require_POST
def adicionar_carrinho(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo, ativo=True)
    
    if not produto.tem_estoque():
        messages.error(request, 'Produto fora de estoque.')
        return redirect('detalhe_produto', codigo=codigo)
    
    item, created = ItemCarrinho.objects.get_or_create(
        user=request.user,
        produto=produto,
        defaults={'quantidade': 1}
    )
    
    if not created:
        if item.quantidade < produto.quantidade:
            item.quantidade += 1
            item.save()
            messages.success(request, f'Quantidade de {produto.nome} atualizada no carrinho.')
        else:
            messages.warning(request, f'Quantidade máxima de {produto.nome} já adicionada.')
    else:
        messages.success(request, f'{produto.nome} adicionado ao carrinho.')
    
    return redirect('carrinho')

@login_required
@require_POST
def remover_carrinho(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    item = get_object_or_404(ItemCarrinho, user=request.user, produto=produto)
    item.delete()
    messages.success(request, f'{produto.nome} removido do carrinho.')
    return redirect('carrinho')

@login_required
@require_POST
def atualizar_quantidade(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    item = get_object_or_404(ItemCarrinho, user=request.user, produto=produto)
    
    nova_quantidade = int(request.POST.get('quantidade', 1))
    
    if nova_quantidade > 0 and nova_quantidade <= produto.quantidade:
        item.quantidade = nova_quantidade
        item.save()
        messages.success(request, 'Quantidade atualizada.')
    else:
        messages.error(request, 'Quantidade inválida.')
    
    return redirect('carrinho')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})