# carts/models.py

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Cliente")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        return f"Carrinho de {self.customer.username}"

    @property
    def total_price(self):
        """Calcula o preço total dos itens no carrinho."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Calcula o número total de itens (quantidade) no carrinho."""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Carrinho")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço na Adição")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado Em")

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ('cart', 'product') # Garante que um produto só aparece uma vez por carrinho

    def __str__(self):
        return f"{self.quantity} x {self.product.name} no carrinho de {self.cart.customer.username}"

    @property
    def total_price(self):
        """Calcula o preço total para este item (quantidade * preço_na_adição)."""
        return self.quantity * self.price_at_addition