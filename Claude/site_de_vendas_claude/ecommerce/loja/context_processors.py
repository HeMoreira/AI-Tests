from .models import ItemCarrinho

def carrinho_context(request):
    if request.user.is_authenticated:
        itens_carrinho = ItemCarrinho.objects.filter(user=request.user)
        total_itens = sum(item.quantidade for item in itens_carrinho)
        total_valor = sum(item.get_subtotal() for item in itens_carrinho)
        total_valor_formatado = f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    else:
        total_itens = 0
        total_valor = 0
        total_valor_formatado = "R$ 0,00"
    
    return {
        'total_itens_carrinho': total_itens,
        'total_valor_carrinho': total_valor,
        'total_valor_carrinho_formatado': total_valor_formatado,
    }
