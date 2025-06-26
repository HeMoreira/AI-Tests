from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=10, unique=True)
    genero = models.CharField(max_length=20, choices=[
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ])
    data_nascimento = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
from carrinho.models import Carrinho

@receiver(post_save, sender=Cliente)
def criar_carrinho_para_cliente(sender, instance, created, **kwargs):
    if created:
        Carrinho.objects.create(cliente=instance)
