from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    categoria_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    
    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome
    
    class Meta:
        verbose_name_plural = "Categorias"

def gerar_codigo_produto():
    return ''.join(random.choices(string.digits, k=5))

class Produto(models.Model):
    PRIORIDADES = [
        (1, 'Muito Alta'),
        (2, 'Alta'),
        (3, 'Normal'),
        (4, 'Baixa'),
        (5, 'Muito Baixa'),
    ]
    
    codigo = models.CharField(max_length=5, unique=True, default=gerar_codigo_produto)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantidade = models.PositiveIntegerField(default=0)
    prioridade = models.IntegerField(choices=PRIORIDADES, default=3)
    categorias = models.ManyToManyField(Categoria, related_name='produtos')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    def get_preco_formatado(self):
        return f"R$ {self.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def tem_estoque(self):
        return self.quantidade > 0
    
    class Meta:
        ordering = ['prioridade', '-data_cadastro']

class PerfilCliente(models.Model):
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    endereco = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"

class ItemCarrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    data_adicao = models.DateTimeField(auto_now_add=True)
    
    def get_subtotal(self):
        return self.produto.preco * self.quantidade
    
    def get_subtotal_formatado(self):
        subtotal = self.get_subtotal()
        return f"R$ {subtotal:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    class Meta:
        unique_together = ['user', 'produto']