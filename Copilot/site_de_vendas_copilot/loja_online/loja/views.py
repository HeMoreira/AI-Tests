from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, Categoria, Carrinho, ItemCarrinho, Cliente
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def pagina_inicial(request):
    destaques = Produto.objects.order_by('-prioridade')[:8]
    return render(request, 'loja/pagina_inicial.html', {'destaques': destaques})

def lista_produtos(request):
    produtos = Produto.objects.all()
    busca = request.GET.get('q')
    categoria = request.GET.getlist('categoria')
    preco_min = request.GET.get('min')
    preco_max = request.GET.get('max')

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    if categoria:
        produtos = produtos.filter(categorias__nome__in=categoria).distinct()

    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)

    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    categorias = Categoria.objects.filter(subcategoria_de__isnull=True)

    return render(request, 'loja/lista_produtos.html', {'produtos': produtos, 'categorias': categorias})

def detalhe_produto(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    return render(request, 'loja/detalhe_produto.html', {'produto': produto})
@login_required
def visualizar_carrinho(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    carrinho, _ = Carrinho.objects.get_or_create(cliente=cliente)
    return render(request, 'loja/carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_carrinho(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    cliente = get_object_or_404(Cliente, user=request.user)
    carrinho, _ = Carrinho.objects.get_or_create(cliente=cliente)

    item, criado = carrinho.itens.get_or_create(produto=produto)
    if not criado:
        item.quantidade += 1
    item.save()
    return redirect('visualizar_carrinho')

@login_required
def remover_carrinho(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    cliente = get_object_or_404(Cliente, user=request.user)
    carrinho = get_object_or_404(Carrinho, cliente=cliente)

    item = carrinho.itens.filter(produto=produto).first()
    if item:
        item.delete()
    return redirect('visualizar_carrinho')
from django.contrib import messages

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'loja/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('pagina_inicial')
from .forms import RegistroUsuarioForm, ClienteForm

def registrar_usuario(request):
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)
        cliente_form = ClienteForm(request.POST)

        if user_form.is_valid() and cliente_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.email = user.email
            cliente.save()
            login(request, user)
            return redirect('pagina_inicial')
    else:
        user_form = RegistroUsuarioForm()
        cliente_form = ClienteForm()

    return render(request, 'loja/registro.html', {'user_form': user_form, 'cliente_form': cliente_form})