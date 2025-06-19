# carts/context_processors.py

from .models import Cart

def cart_items_count(request):
    """
    Adiciona o número de itens no carrinho ao contexto de todos os templates.
    """
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(customer=request.user)
            cart_item_count = cart.total_items
        except Cart.DoesNotExist:
            pass
    return {'cart_item_count': cart_item_count}