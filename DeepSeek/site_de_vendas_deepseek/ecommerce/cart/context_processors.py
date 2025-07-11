from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)
        return {'cart': cart}
    return {'cart': None}