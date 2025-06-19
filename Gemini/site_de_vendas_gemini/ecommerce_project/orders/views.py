# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction # Para garantir atomicidade na criação do pedido
from carts.models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm

@login_required
def checkout_view(request):
    """
    Exibe a página de checkout para o usuário finalizar o pedido.
    """
    cart = get_object_or_404(Cart, customer=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.warning(request, "Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.")
        return redirect('product_list')

    # Pré-preenche o formulário de checkout com dados do perfil do cliente
    initial_data = {
        'shipping_address': request.user.profile.address,
        'zip_code': request.user.profile.zip_code,
        'city': request.user.profile.city,
        'state': request.user.profile.state,
        'country': request.user.profile.country,
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            try:
                with transaction.atomic(): # Garante que todas as operações ocorram ou nenhuma ocorra
                    # 1. Verificar estoque novamente antes de criar o pedido
                    for item in cart_items:
                        product = item.product
                        if not product.is_active or product.quantity < item.quantity:
                            messages.error(request, f"Desculpe, '{product.name}' não tem mais a quantidade desejada em estoque.")
                            return redirect('cart_detail') # Volta para o carrinho

                    # 2. Criar o Pedido
                    order = Order.objects.create(
                        customer=request.user,
                        total_amount=cart.total_price,
                        shipping_address=f"{form.cleaned_data['shipping_address']}\n"
                                         f"CEP: {form.cleaned_data['zip_code']}\n"
                                         f"{form.cleaned_data['city']}/{form.cleaned_data['state']}, {form.cleaned_data['country']}",
                        payment_method=form.cleaned_data['payment_method'],
                        status='Pendente', # Ou 'Processando' dependendo do seu fluxo de pagamento
                        payment_status='Pendente'
                    )

                    # 3. Mover Itens do Carrinho para Itens do Pedido e Atualizar Estoque
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            quantity=item.quantity,
                            price_at_purchase=item.price_at_addition,
                            total_item_price=item.total_price
                        )
                        # Reduzir o estoque do produto
                        product = item.product
                        product.quantity -= item.quantity
                        product.save()

                    # 4. Limpar o carrinho
                    cart.items.all().delete()
                    cart.delete() # Opcional: pode manter o carrinho e limpar os itens

                    messages.success(request, "Seu pedido foi realizado com sucesso!")
                    return redirect('order_confirmation', order_number=order.order_number)

            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao finalizar seu pedido: {e}. Por favor, tente novamente.")
                return redirect('cart_detail') # Redireciona de volta em caso de erro
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation_view(request, order_number):
    """
    Exibe a página de confirmação de um pedido.
    """
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'orders/order_confirmation.html', context)

@login_required
def order_list_view(request):
    """
    Lista todos os pedidos do usuário logado.
    """
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail_view(request, order_number):
    """
    Exibe os detalhes de um pedido específico do usuário logado.
    """
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'orders/order_detail.html', context)