from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product, Category
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    featured_products = Product.objects.filter(priority='H')[:8]
    new_products = Product.objects.order_by('-date_added')[:4]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'products/home.html', context)

def product_list(request):
    products = Product.objects.all().order_by('-priority', '-date_added')
    
    # Filtering
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(categories=category)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(parent__isnull=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(categories__in=product.categories.all()).exclude(pk=pk).distinct()[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(categories=category).order_by('-priority', '-date_added')
    subcategories = category.subcategories.all()
    
    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
    }
    return render(request, 'products/category_products.html', context)