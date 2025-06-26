from django.db import models
from clientes.models import Cliente
from produtos.models import Produto

class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f'Carrinho de {self.cliente.user.username}'

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    adicionado_em = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'
