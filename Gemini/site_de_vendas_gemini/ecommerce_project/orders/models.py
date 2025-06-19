# orders/models.py

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import uuid # Para gerar order_number únicos

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Enviado', 'Enviado'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago'),
        ('Reembolsado', 'Reembolsado'),
        ('Falha', 'Falha'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='orders', verbose_name="Cliente")
    order_number = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Número do Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente', verbose_name="Status do Pedido")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    shipping_address = models.TextField(verbose_name="Endereço de Entrega")
    payment_method = models.CharField(max_length=50, verbose_name="Método de Pagamento")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pendente', verbose_name="Status do Pagamento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização do Pedido")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.order_number} - {self.customer.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).upper()[:8] # Gera um número de pedido curto
            while Order.objects.filter(order_number=self.order_number).exists():
                self.order_number = str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produto")
    product_name = models.CharField(max_length=255, verbose_name="Nome do Produto (Histórico)")
    quantity = models.IntegerField(verbose_name="Quantidade")
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço na Compra")
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Total do Item")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantity} x {self.product_name} em Pedido #{self.order.order_number}"