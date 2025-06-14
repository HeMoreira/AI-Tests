from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    subcategoria_de = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategorias')

    class Meta:
        verbose_name_plural = "Categorias"
        unique_together = ('nome', 'subcategoria_de')

    def __str__(self):
        return f"{self.subcategoria_de.nome + ' > ' if self.subcategoria_de else ''}{self.nome}"

class Produto(models.Model):
    codigo = models.CharField(max_length=5, unique=True)  # 5 algarismos
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=200)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    prioridade = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(default=timezone.now)
    categorias = models.ManyToManyField(Categoria, related_name='produtos')

    class Meta:
        ordering = ['-prioridade', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    identificador = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    genero = models.CharField(max_length=15, choices=[("masculino", "Masculino"), ("feminino", "Feminino"), ("outro", "Outro")])
    data_nascimento = models.DateField()
    data_cadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='carrinho')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Carrinho de {self.cliente.nome}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrinho', 'produto')

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"
