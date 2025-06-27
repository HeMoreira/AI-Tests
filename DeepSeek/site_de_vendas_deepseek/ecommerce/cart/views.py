from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Product added to cart!')
    return redirect('cart-detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, customer=request.user)
    
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    
    messages.success(request, 'Product removed from cart!')
    return redirect('cart-detail')

@login_required
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, customer=request.user)
    
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    else:
        cart_item.delete()
        messages.success(request, 'Product removed from cart!')
    
    return redirect('cart-detail')