# products/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q # Para buscas complexas
from .models import Product, Category

def product_list_view(request, category_slug=None):
    """
    Exibe a lista de produtos, com opções de filtragem e ordenação.
    """
    products = Product.objects.filter(is_active=True)
    current_category = None

    # Filtragem por Categoria
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        # Inclui produtos da categoria principal e suas subcategorias
        descendants = current_category.get_descendants(include_self=True) # Requere django-mptt para get_descendants
        products = products.filter(categories__in=descendants).distinct()
        # Se não for usar django-mptt, teria que fazer uma busca recursiva manual ou simplificar
        # products = products.filter(categories=current_category)


    # Busca por query (nome, descrição curta)
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).distinct() # distinct() para evitar duplicatas se um produto estiver em várias categorias e corresponder à busca

    # Filtragem por preço
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Filtragem por promoção (exemplo simples)
    if request.GET.get('promo'):
        products = products.filter(price__lt=100) # Exemplo: produtos abaixo de R$100 são promo

    # Ordenação
    sort_by = request.GET.get('sort', 'priority') # Padrão: prioridade
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else: # Default: priority
        products = products.order_by('priority', '-created_at')

    # Paginação
    paginator = Paginator(products, 12) # 12 produtos por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'current_category': current_category,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Exibe os detalhes de um produto específico.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    # Produtos relacionados (exemplo simples: da mesma categoria principal)
    related_products = Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(slug=slug).distinct()[:4] # Limite de 4 produtos relacionados

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)