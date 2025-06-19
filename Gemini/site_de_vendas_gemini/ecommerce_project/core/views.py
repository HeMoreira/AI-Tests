# core/views.py

from django.shortcuts import render
from products.models import Product, Category

def home_view(request):
    """
    Exibe a página inicial com produtos em destaque, promoções e novidades.
    """
    featured_products = Product.objects.filter(is_active=True, priority__lt=5).order_by('priority', '-created_at')[:8]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    # Poderíamos ter um campo 'is_promo' ou uma lógica de desconto para promoções
    promotional_products = Product.objects.filter(is_active=True, price__lt=100).order_by('?')[:8] # Exemplo simples

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'promotional_products': promotional_products,
    }
    return render(request, 'core/home.html', context)