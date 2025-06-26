from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    categoria_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategorias')

    def __str__(self):
        return self.nome

class Produto(models.Model):
    identificador = models.CharField(max_length=5, unique=True)
    nome = models.CharField(max_length=200)
    categorias = models.ManyToManyField(Categoria)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=255)
    prioridade = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=10, unique=True)
    genero = models.CharField(max_length=10, choices=[("Masculino", "Masculino"), ("Feminino", "Feminino"), ("Outro", "Outro")])
    data_nascimento = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username

class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    adicionado_em = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.produto.preco * self.quantidade


class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemCarrinho)

    def total(self):
        return sum([item.subtotal() for item in self.itens.all()])

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemCarrinho)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.usuario.username}"

class Promocao(models.Model):
    nome = models.CharField(max_length=100)
    percentual_desconto = models.FloatField()  # exemplo: 10.0 para 10%
    produtos = models.ManyToManyField(Produto)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

def info_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    promocao = Promocao.objects.filter(produtos=produto, ativa=True).first()
    preco_final = produto.preco
    if promocao:
        preco_final -= preco_final * (promocao.percentual_desconto / 100)
    return render(request, 'loja/info_produto.html', {
        'produto': produto,
        'promocao': promocao,
        'preco_final': round(preco_final, 2)
    })
