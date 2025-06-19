# products/models.py

from django.db import models
from django.utils.text import slugify
import random
import string

def generate_sku():
    """Gera um SKU alfanumérico único de 5 caracteres."""
    while True:
        sku = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if not Product.objects.filter(sku=sku).exists():
            return sku

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name="Categoria Pai")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição da Categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    sku = models.CharField(max_length=5, unique=True, default=generate_sku, verbose_name="SKU")
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    categories = models.ManyToManyField(Category, related_name='products', verbose_name="Categorias")
    quantity = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição Completa")
    short_description = models.CharField(max_length=150, verbose_name="Descrição Curta")
    priority = models.IntegerField(default=1, verbose_name="Prioridade de Exibição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagem do Produto")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['priority', 'name'] # Ordenação padrão

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.quantity > 0