from django.shortcuts import render, get_object_or_404
from .models import Produto

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produtos/detalhes.html', {'produto': produto})
