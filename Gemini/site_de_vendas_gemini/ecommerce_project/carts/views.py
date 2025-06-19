# carts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

@login_required
def cart_detail_view(request):
    """
    Exibe o conteúdo do carrinho de compras do usuário logado.
    """
    cart, created = Cart.objects.get_or_create(customer=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'carts/cart_detail.html', context)

@login_required
def add_to_cart(request, sku):
    """
    Adiciona um produto ao carrinho ou atualiza sua quantidade.
    """
    product = get_object_or_404(Product, sku=sku, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        messages.error(request, "A quantidade deve ser pelo menos 1.")
        return redirect('product_detail', slug=product.slug)

    if not product.is_in_stock or product.quantity < quantity:
        messages.error(request, f"Desculpe, temos apenas {product.quantity} unidades de '{product.name}' em estoque.")
        return redirect('product_detail', slug=product.slug)

    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity, 'price_at_addition': product.price}
    )

    if not item_created:
        # Se o item já existe, atualiza a quantidade
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.quantity:
            messages.error(request, f"Não é possível adicionar mais. Você já tem {cart_item.quantity} unidades e há {product.quantity} em estoque de '{product.name}'.")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Quantidade de '{product.name}' atualizada no carrinho.")
    else:
        messages.success(request, f"'{product.name}' foi adicionado ao seu carrinho!")

    # Redireciona para o carrinho ou para a página anterior
    next_url = request.POST.get('next', 'cart_detail')
    return redirect(next_url)

@login_required
def remove_from_cart(request, sku):
    """
    Remove um item específico do carrinho.
    """
    cart = get_object_or_404(Cart, customer=request.user)
    product = get_object_or_404(Product, sku=sku) # Não precisa de is_active aqui, pois está removendo

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        product_name = cart_item.product.name # Salva o nome antes de deletar o item
        cart_item.delete()
        messages.info(request, f"'{product_name}' foi removido do seu carrinho.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item não encontrado no seu carrinho.")

    return redirect('cart_detail')

@login_required
def update_cart_quantity(request, sku):
    """
    Atualiza a quantidade de um item no carrinho.
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, sku=sku, is_active=True)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity <= 0:
            messages.error(request, "A quantidade deve ser pelo menos 1. Se deseja remover, use o botão Remover.")
            return redirect('cart_detail')

        cart = get_object_or_404(Cart, customer=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

        if new_quantity > product.quantity:
            messages.error(request, f"Desculpe, a quantidade máxima disponível para '{product.name}' é {product.quantity}.")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Quantidade de '{product.name}' atualizada para {new_quantity}.")
    return redirect('cart_detail')